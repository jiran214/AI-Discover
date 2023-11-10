from typing import List

import pytest
from bilibili_api import search
from bilibili_api.video import Video

from spider import base
from schema.base import Summary, Outline, Fragment
from schema.bilibili import BiliNoteView
from schema.note import BilibiliNote
from utils import get_credential


class VideoSpider(base.NoteSpider):

    def __init__(self, credential=None):
        self.credential = credential or get_credential()
        self.credential.raise_for_no_sessdata()
        self.credential.raise_for_no_buvid3()

    async def get_note_search_list(
            self, query, top_n=20, *args, **kwargs
    ) -> List[Video]:
        for page in range(1, top_n // 20 + 2):
            resp = await search.search(keyword=query)
            video_list = []
            res_list = resp['result']
            for res_item in res_list:
                if res_item['result_type'] == 'video':
                    for item in res_item['data']:
                        video = Video(aid=item['aid'], credential=self.credential)
                        video_list.append(video)
                        if len(video_list) >= top_n:
                            return video_list

        # return await search.search(
        #     query,
        #     search_type=search.SearchObjectType.VIDEO,
        #     order_type=search.OrderVideo.SCORES, time_range=10,
        #     video_zone_type=video_zone.VideoZoneTypes.,
        #     page=1,
        #     debug_param_func=print
        # )

    async def get_note_detail(self, video: Video):
        info = await video.get_info()
        return BiliNoteView(**info)

    async def get_note_summary(self, video: Video) -> Summary:
        """获取AI总结"""
        page_index = 0
        json_data = await video.get_ai_conclusion(page_index=page_index)
        assert json_data['code'] == 0, '没有权限'
        model_result = json_data['model_result']
        aid = video.get_aid()
        summary_info = Summary(
            content=model_result['summary'],
            metadata={'aid': aid},
            outlines=[
                Outline(
                    fragments=[
                        Fragment(
                            content=part_outline['content'],
                            metadata={'timestamp': part_outline['timestamp'], 'aid': aid}
                        )
                        for part_outline in outline['part_outline']
                    ],
                    content=outline['title'],
                    metadata={'timestamp': outline['timestamp'], 'aid': aid}
                )
                for outline in model_result['outline']
            ]
        )
        return summary_info

    async def get_notes(self, query, top_n=20) -> List[BilibiliNote]:
        video_list = await self.get_note_search_list(query, top_n)
        notes = []
        for video in video_list:
            try:
                view = await self.get_note_detail(video)
                assert video._Video__info
                summary = await self.get_note_summary(video)
                assert summary
            except Exception as e:
                raise e
            notes.append(BilibiliNote(summary=summary, view=view))
            # break
        return notes


@pytest.mark.asyncio
async def test_get_notes():
    spider = VideoSpider()
    notes = await spider.get_notes(query='仲尼', top_n=5)
    print(notes)
    assert len(notes) == 5
