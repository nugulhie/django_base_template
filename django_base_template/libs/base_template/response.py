from rest_framework.response import Response


class ReturnResponse(Response):
    def __init__(
        self,
        data=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
        flag=False,
    ):
        """
        data 딕셔너리의 형태를 변경해서 반환하는 데이터 형태를 변경한다.
        """
        data = {"success": flag, "data": data}
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )