from osbot_fast_api.api.routes.Routes__Set_Cookie            import Routes__Set_Cookie
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API import Serverless__Fast_API
from osbot_fast_api_serverless.fast_api.routes.Routes__Info  import Routes__Info
from mgraph_ai_service_aws.config                           import FAST_API__TITLE, FAST_API__DESCRIPTION
from mgraph_ai_service_aws.utils.Version                    import version__mgraph_ai_service_aws


class AWS__Service__Fast_API(Serverless__Fast_API):

    def setup(self):
        with self.config as _:
            _.name           = FAST_API__TITLE
            _.version        = version__mgraph_ai_service_aws
            _.description    = FAST_API__DESCRIPTION
        return super().setup()

    def setup_routes(self):
        self.add_routes(Routes__Info        )
        self.add_routes(Routes__Set_Cookie  )



