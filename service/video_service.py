class VideoService:

    def __init__(self, video_id: str):
        self.video_id = video_id

    def create_video(self) -> dict:

        # TODO 데이터베이스 읽기 -> 이미 존재하면 database에서 읽은 데이터 리턴

        from pytubefix import YouTube
        from pytubefix.cli import on_progress

        url = f"https://youtu.be/{self.video_id}"
        yt = YouTube(url, on_progress_callback=on_progress)  # TODO 내부 래퍼로 구현

        from model.controller import VideoCreateResponse

        response_fields = VideoCreateResponse.model_fields.keys()
        res = {field: getattr(yt, field, None) for field in response_fields}
        res["video_id"] = self.video_id
        if res["thumbnail_url"] is None:
            res["thumbnail_url"] = f"https://i.ytimg.com/vi/{self.video_id}/hq2.jpg"

        # TODO: res 데이터베이스 저장
        return res
