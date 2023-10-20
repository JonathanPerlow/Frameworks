from sanic import response


class CustomResponse:

    @staticmethod
    def json_not_found(item, message="Not found"):
        """
           This response return a 404 status.
        """
        return response.json({"error": f"{item} {message}"}, status=404)

    @staticmethod
    def json_ok(item, message="found"):
        """
           This response return a 200 status.
        """
        return response.json({"error": f"{item} {message}"}, status=200)

    @staticmethod
    def json_ok(item, message="found"):
        """
           This response return a 200 status.
        """
        return response.json({"error": f"{item} {message}"}, status=200)