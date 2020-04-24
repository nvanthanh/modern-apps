from aws_cdk import core
from aws_cdk import aws_dynamodb, aws_lambda, aws_apigateway

from base_common import BaseStack

# Our main Application Stack
class UrlShortenerStack(BaseStack):
# class UrlShortenerStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        
        ## Define the table that maps short codes to URLs.
        table = aws_dynamodb.Table(self, "mapping-table",
                partition_key=aws_dynamodb.Attribute(
                    name="id",
                    type=aws_dynamodb.AttributeType.STRING),
                read_capacity=10,
                write_capacity=5)
                
        ## Defines Lambda resource & API-Gateway request handler
        ## All API requests will go to the same function.
        handler = aws_lambda.Function(self, "UrlShortenerFunction",
                            code=aws_lambda.Code.asset("./lambda"),
                            handler="handler.main",
                            timeout=core.Duration.minutes(5),
                            runtime=aws_lambda.Runtime.PYTHON_3_7)

        ## Pass the table name to the handler through an env variable 
        ## and grant the handler read/write permissions on the table.
        table.grant_read_write_data(handler)
        handler.add_environment('TABLE_NAME', table.table_name)
        
        ## Define the API endpoint and associate the handler
        api = aws_apigateway.LambdaRestApi(self, "UrlShortenerApi",
                                           handler=handler)

        ## Map shortener.aws.job4u.io to this API Gateway endpoint
        ## The shared Domain Name that can be accessed through the API in BaseStack
        ## NOTE: you can comment out if you want to bypass the Domain Name mapping
        self.map_base_subdomain('shortener', api)
