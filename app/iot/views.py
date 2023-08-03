from json import dumps
import json
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated


from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from boto3.dynamodb.conditions import Key
from assests.models import Alert, Asset, Rule

from assests.serializers import AlertSerializer


import boto3
import environ
import pusher

env = environ.Env()
environ.Env.read_env()

# Create your views here.

class HandleIotThings(APIView):
    permission_classes = [IsAuthenticated,]
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.thing_client = boto3.client(
            'iot', 
            env('REGION'),
            aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY'),
        )
        self.dynamodb = boto3.resource(
            'dynamodb',
            env('REGION'),
            aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY')
        )
        self.table = self.dynamodb.Table('ThingsTable')

    
    def get(self,request,id):
        try:
            get_response = self.table.query(
                KeyConditionExpression=Key('asset_id').eq(id),
            )
            return Response(get_response.get('Items'),status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    @csrf_exempt 
    def post(self,request,id):
        try:
            thing_name = request.data.get('thing_name')
            thing_type_name = request.data.get('thing_type_name')
            asset_id = request.data.get('asset_id')
            create_thing_response = self.thing_client.create_thing(
                                thingName=thing_name,
                                thingTypeName=thing_type_name
                            )
            # Create Certificates                 
            certificate_response = self.thing_client.create_keys_and_certificate(
                setAsActive=True
            )
            # Attach Certificates to thing
            attach_thing_response = self.thing_client.attach_thing_principal(
                thingName=thing_name,
                principal=certificate_response.get('certificateArn')
            )
            
            thing_id = create_thing_response.get('thingId')
            certificate_arn = certificate_response.get('certificateArn')
            certificate_id = certificate_response.get('certificateId')
            public_key = certificate_response.get('keyPair').get('PublicKey')[27:-26]
            private_key = certificate_response.get('keyPair').get('PrivateKey')[32:-31]
            self.table.put_item(
                Item = {
                    'user_id':id,
                    'asset_id':asset_id,
                    'thing_id':thing_id,
                    'thing_name':thing_name,
                    'thing_type_name':thing_type_name,
                    'certificate_arn':certificate_arn,
                    'certificate_id':certificate_id,
                    'public_key':public_key,
                    'private_key':private_key,
                }
            )
            return Response(create_thing_response,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
            

class HandleSendCommand(APIView):
    permission_classes = [AllowAny,]
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.client = boto3.client(
            'iot-data', 
            env('REGION'),
            aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY'),
        )
        
    @csrf_exempt
    def post(self,request):
        
        topic = "MindOptimizerAssetTopic"
        
        publish_response = self.client.publish(topic=topic, payload=dumps(request.data))
        
        return Response(publish_response)


class HandleGetDataView(APIView):
    permission_classes = [AllowAny,]
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.pusher_client = pusher.Pusher(
            app_id= env('APP_ID'),
            key= env('KEY'),
            secret= env('SECRET'),
            cluster= env('CLUSTER'),
            ssl=True
        )
        self.dynamodb = boto3.resource(
            'dynamodb',
            env('REGION'),
            aws_access_key_id = env('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = env('AWS_SECRET_ACCESS_KEY')
        )
        self.table = self.dynamodb.Table('AssetDataTable')
        
    def get(self,request,id):
        try:
            get_response = self.table.query(
                KeyConditionExpression=Key('user_id').eq(id),
            )
            return Response(get_response.get("Items"),status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    # def create_ale
        
    @csrf_exempt    
    def post(self,request):
        try:
            
            self.table.put_item(
                Item=request.data
            )
            response = request.data
            rule_obj = Rule.objects.filter(asset_id = request.data.get('asset_id'))
                       
            for rule in rule_obj:
               
                subject = "Regarding Alerts"
              
                if rule.condition == 'temperature' and int(response.get('temperature')) > int(rule.value):
                    message = f"your assets {rule.asset.vehicle_number}  temperature is greater than set threshold."                    
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [rule.asset.user.email], fail_silently=False)
                    
                    data = {
                        "alert_type":f"Temperature-{rule.asset.id}",
                        "value":response.get('temperature'),
                        "alert_condition":rule.condition,
                        "user":rule.asset.user,
                        "message":message
                    }
                    alert = Alert(**data)
                    alert.save()
                    alert.asset.add(rule.asset.id)
                    self.pusher_client.trigger(u'MindOptimizerAssetTopic', u'Alert-6787f95d-17fc-5c2c-7bbf-4f88eb3ea2c7', response)

                if rule.condition == 'speed' and int(response.get('speed')) > int(rule.value):
                    message = f"your assets {rule.asset.vehicle_number} speed is greater than set threshold."                    
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [rule.asset.user.email], fail_silently=False)
                    data = {
                        "alert_type":f"Temperature-{rule.asset.id}",
                        "value":response.get('speed'),
                        "alert_condition":rule.condition,
                        "user":rule.asset.user,
                        "message":message
                    }
                    alert = Alert(**data)
                    alert.save()
                    alert.asset.add(rule.asset.id)
                    self.pusher_client.trigger(u'MindOptimizerAssetTopic', u'Alert-6787f95d-17fc-5c2c-7bbf-4f88eb3ea2c7', response)
                
                if rule.condition == 'fuel' and int(response.get('fuel')) < int(rule.value):
                    message = f"your assets {rule.asset.vehicle_number} fuel is less than set threshold."                    
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [rule.asset.user.email], fail_silently=False)
                    data = {
                        "alert_type":f"Temperature-{rule.asset.id}",
                        "value":response.get('fuel'),
                        "alert_condition":rule.condition,
                        "user":rule.asset.user,
                        "message":message
                    }
                    alert = Alert(**data)
                    alert.save()
                    alert.asset.add(rule.asset.id)
                    self.pusher_client.trigger(u'MindOptimizerAssetTopic', u'Alert-6787f95d-17fc-5c2c-7bbf-4f88eb3ea2c7', response)

            
                response_1  = self.pusher_client.trigger(u'MindOptimizerAssetTopic', u'6787f95d-17fc-5c2c-7bbf-4f88eb3ea2c7', response)
                print(response_1,"*"*50)
            return Response(response)
        
        except Exception as e:
            return Response({"Error":str(e)},status=status.HTTP_400_BAD_REQUEST)
        
        
