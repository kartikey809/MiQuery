from asyncio import run
import sys
from django.shortcuts import redirect, render, HttpResponse
from . models import Results
from . forms import *
from django.db.models import Q
from django.http import JsonResponse
from subprocess import run,PIPE
from Query_functions import *

# embeddings = OpenAIEmbeddings()
# db = FAISS.from_texts(['''
# { "Feed Name" : "LLD Impressions Feed",
# "Description": "A timestamp level data of advertisment impressions served by us",
# "schema" : {"LLD_user_id": {"Description": 'cookie id for the relevant impression, unique to LLD', "datatype": "string"},
#       "LLD_device_id": {"Description": 'device id of device where the relevant impression was served', "datatype": "string"},
#       "ts": {"Description": "Time stamp of impression served", "datatype": "timestamp"},
#       "campaign_id" : {"Description": "ID of campaign that is running", "datatype": "string"},
#       "advertiser_id" : {"Description": "ID of advertiser for whom the campaign is running", "datatype": "string"},
#       "Country" : {"Description": "two digit country code where the impression was served", "datatype": "string"}}
# }
# ''',
#         '''{ "Feed Name" : "Audience Data",
# "Description": "A third part audience dataset mapping user ids from LLD feed to relevant audience segment ids",
# "schema" : {"LLD_user_id": {"Description": 'cookie id unique to LLD', "datatype": "string"},
#       "segment_id": {"Description": "Unique Identifier of the audience segment", "datatype": "string"}
# }''',
#         '''{ "Feed Name" : "Audience Data Mapper",
# "Description": "A third part audience dataset mapping user ids from LLD feed to relevant audience segment ids",
# "schema" : {"segment_id": {"Description": 'Unique Identifier of the audience segment', "datatype": "string"},
#       "segment_name": {"Description": "Name mapping for the unique identifier", "datatype": "string"}
# }
# ''',
#         '''
# { "Feed Name" : "Location Footfall data",
# "Description": "A timestamp level data of footfall around a store defined by a set radius (usually ~200m radius)",
# "schema" : {"LLD_device_id": {"Description": "Device id of the device located within the radius', "datatype": "string"},
#       "ts": {"Description": "Time stamp of when the device entered the radius", "datatype": "timestamp"},
#       "Lat" : {"Description": "Lattitude of device upon entering the radius", "datatype": "string"}},
#       "Long" : {"Description": "Longitude of device upon entering the radius", "datatype": "string"}},
#       "store_name" : {"Description": "Store Name around which the radius is set", "datatype": "string"}}
# }''',
#  '''
# {   "Feed Name" : "Tapad Feed OR cross device feed",
#     "Description": "Tapad provides us with cross-device graph for North Amerca and APAC region. This graph will be refreshed weekly and have a maximum of 60 day look back.",
#     "schema" : {
#       "household_id": {"Description": "A unique ID that denotes a household. If there is more than one person in a household, the value will repeat for each Individual ID", "datatype": "string"},
#       "country_code": {"Description": "This field holds the three letter county code. e.g. USA for US, IND for India", "datatype": "string"},
#       "individuals_individual_id": {"Description": "A unique ID that denotes a person. If there is more than one device under a person, the value will repeat for each identifier", "datatype": "timestamp"},
#       "individuals_devices_device_id" : {"Description": "This field represents the canonical id. It's mostly used for internal connection/processing", "datatype": "BIGINT"},
#       "individuals_devices_ids_type" : {"Description": "Denotes the type of id among HARDWARE_IDFA, HARDWARE_ANDROID_, TTD, APN", "datatype": "string"},
#       "individuals_devices_ids_value" : {"Description": "This field contains Cookie ID or Device ID. We can segregate cookie ids and device ids using individuals_devices_ids_type field.", "datatype": "string"}
#     }
# }''',
#     '''
# {   "Feed Name" : "samba commercial feed OR TV commercial feed",
#     "Description": "samba provides with viewership information about the content that is displayed on opted-in television sets, including Movies,Shows,Sports,Ads",
#     "schema" : {
#         "smba_id" : {"Description": "Unique TV Identifier" , "datatype": "string"},
#         "schedule_ts" : {"Description": "Scheduled time stamp of the commercial" , "datatype": "bigint"},
#         "exposure_ts" : {"Description": "exposed time stamp of the commercial" , "datatype": "bigint"},
#         "network" : {"Description": "Network at which the commercial was displayed" , "datatype": "string"},
#         "network_id" : {"Description": "Unique network identifier" , "datatype": "string"},
#         "prior_title" : {"Description": "The show before the commercial" , "datatype": "string"},
#         "prior_title_id" : {"Description": "Unique identifier of the show before the commercial" , "datatype": "string"},
#         "next_title" : {"Description": "The show after the commercial" , "datatype": "string"},
#         "next_title_id" : {"Description": "Unique identifier of the show after the commercial" , "datatype": "string"},
#         "advertiser" : {"Description": "Advertiser associated with the commercial" , "datatype": "string"},
#         "advertiser_id" : {"Description": "Unique Identifier for the advertiser associated with the commercial" , "datatype": "string"},
#         "brand" : {"Description": "Brand associated with the commercial" , "datatype": "string"},
#         "brand_id" : {"Description": "Unique Identifier for the Brand associated with the commercial" , "datatype": "string"},
#         "product" : {"Description": "Product associated with the commercial" , "datatype": "string"},
#         "product_id" : {"Description": "Unique Identifier for the Product associated with the commercial" , "datatype": "string"},
#         "tv_spot_name" : {"Description": "Commercial Name" , "datatype": "string"},
#         "tv_spot_id" : {"Description": "Unique Identifier for the Commercial Name" , "datatype": "string"},
#         "duration" : {"Description": "Duration of the commercial" , "datatype": "bigint"},
#         "zip" : {"Description": "Zip Code" , "datatype": "string"}
#     }
# }''',
#   '''
#   { "Feed Name" : "samba IP feed OR TV IP feed",
#     "Description": "samba IP feed provides with viewership information about the content that is displayed on opted-in television sets, including Movies,Shows,Sports,Ads and tracks user information through their IP addresses",
#     "schema" : {
#         "smba_id" : {"Description": "Unique TV Identifier" , "datatype": "string"},
#         "ip_address" : {"Description": "IP address" , "datatype": "string"},
#         "date" : {"Description": "Date related to the Impression" , "datatype": "timestamp"},
#         "postal_code" : {"Description": "Postal Code at which TV exists" , "datatype": "string"}
#     }
# }
# ''',
#          '''
#   { "Feed Name" : "pixel feed OR conversion feed",
#     "Description": "This Feed provides data on the firing of all of advertisers' pixels or conversions, both attributed and unattributed.",
#     "schema" : {
#         "dt" : {"Description": "The time and date of the conversion" , "datatype": "timestamp"},
#         "user_id_64" : {"Description": "cookie id for the relevant conversion, unique to feed" , "datatype": "string"},
#         "pixel_id" : {"Description": "The ID of the conversion pixel." , "datatype": "int"},
#         "http_referer" : {"Description": "The entire URL where conversion pixel fired" , "datatype": "string"}
#     }
# }
# ''',
#          '''
#   {  "Feed Name" : "pixel server feed OR capture feed OR advance pixel feed",
#     "Description": "Data passed on through Advanced Pixels, usually used to look at the u-variables passed on at the time of pixel fire. Typically used for advanced analytics for optimizations and insights",
#     "schema" : {
#         "dt" : {"Description": "The time and date of the conversion" , "datatype": "timestamp"},
#         "UID" : {"Description": "cookie id for the relevant conversion, unique to feed" , "datatype": "string"},
#         "pixel_id" : {"Description": "The ID of the conversion pixel." , "datatype": "int"},
#         "referer" : {"Description": "The entire URL where conversion pixel fired" , "datatype": "string"},
#         "Advance Variables" : {"Description": "25 variables from u1 to u25 containing Information passed through the pixel is captured in these columns" , "datatype": "string"}
#     }
# }
#          ''',
#       '''
#   { "Feed Name" : "universal pixel feed",
#     "Description": "This Feed provides data on the firing of all of advertisers' pixels or conversions, both attributed and unattributed.",
#     "schema" : {
#         "date_time" : {"Description": "The time and date of the conversion" , "datatype": "timestamp"},
#         "user_id_64" : {"Description": "cookie id for the relevant conversion, unique to feed" , "datatype": "string"},
#         "pixel_uuid" : {"Description": "The UUID of the universal pixel." , "datatype": "string"},
#         "http_referer" : {"Description": "The entire URL where universal pixel fired" , "datatype": "string"},
#         "conversion_pixel_ids" : {"Description": "The list of IDs for the conversion events triggered by the user as a result of the universal pixel firing" , "datatype": "string"},
#         "device_unique_id" : {"Description": "The unique identifier representing the device" , "datatype": "string"}
#     }
# }
# ''',
#   '''
#   {
# "Feed Name" : "video event feed OR video feed",
# "Description": "A timestamp level data of video advertisment impressions served by us",
# "schema" : {
#         "LLD_user_id_64": {"Description": "cookie id for the relevant impression, unique to LLD", "datatype": "string"},
#         "LLD_device_id": {"Description": "device id of device where the relevant impression was served", "datatype": "string"},
#         "date_time": {"Description": "Time stamp of impression served", "datatype": "timestamp"},
#         "campaign_id" : {"Description": "ID of campaign that is running", "datatype": "string"},
#         "advertiser_id" : {"Description": "ID of advertiser for whom the campaign is running", "datatype": "string"},
#         "country" : {"Description": "two digit country code where the impression was served", "datatype": "string"},
#         "insertion_order_id" : {"Description": "The ID for insertion order if used.", "datatype": "string"},
#         "line_item_id" : {"Description": "two digit country code where the impression was served", "datatype": "string"},
#         "creative_id" : {"Description": "The ID of the creative served", "datatype": "string"},
#         "video_hit_25_pct" : {"Description": "Whether or not the video hit 25 pct this hour" , "datatype": "boolean"},
#         "video_hit_50_pct" : {"Description": "Whether or not the video hit 50 pct this hour" , "datatype": "boolean"},
#         "video_hit_75_pct" : {"Description": "Whether or not the video hit 75 pct this hour" , "datatype": "boolean"},
#         "video_completed" : {"Description": "Whether or not the video completed this hour" , "datatype": "boolean"}
#     }
# }
# ''',
#     '''
#   { "Feed Name" : "DPI feed",
#     "Description": "Log level data for all the auctions that were processed by all instances of Xandr/Appnexus. contains Pre-bid data, Auctions won, Auctions lost and Auctions that we never bid on",
#     "schema" : {
#         "dpi_TimeStamp" : {"Description": "The time and date of the auction" , "datatype": "timestamp"},
#         "UserId" : {"Description": "cookie id for the relevant conversion, unique to feed" , "datatype": "string"},
#         "degeocountry" : {"Description": "the three digit country code" , "datatype": "string"},
#         "refererUrl" : {"Description": "The entire URL where conversion pixel fired" , "datatype": "string"}
#     }
#   }
# '''
# ], embeddings)
# with open("Faiss_Schema.txt", "wb") as binary_file:
#         binary_file.write(db.serialize_to_bytes())

# db = FAISS.from_texts(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'], embeddings)
# with open("Faiss_Code.txt", "wb") as binary_file:
#         binary_file.write(db.serialize_to_bytes())        

# Create your views here.
def home(request):
    return render(request,'firstapp/index.html')
    

def explore(request):
   print('index')
   if 'qry' in request.GET:
         q = request.GET['qry']
         all_q = Q((Q(usecase__icontains=q))  | (Q(title__icontains=q) | Q(description__icontains=q)))
         resp = Results.objects.filter(all_q).order_by('-upvote')
   else:    
      resp = Results.objects.all()
      resp = resp.order_by('-upvote')
   context={
         'resp':resp
      }
   return render(request, 'firstapp/explore.html',context) 

# def home(request,usecase):
#    if usecase in ['dna','eng','tech']:
#    # if True:
#       print('Home True')
#       if 'qry' in request.GET:
#          q = request.GET['qry']
#          all_q = Q((Q(usecase__icontains=q))  | (Q(title__icontains=q) | Q(description__icontains=q)))
#          resp = Results.objects.filter(all_q).order_by('-upvote')

#       else:
#          usecase_q = Q(Q(usecase__icontains=usecase))
#          resp = Results.objects.filter(usecase_q).order_by('-upvote')
#       context = {
#          'resp':resp
#       }
#       return render(request, 'firstapp/home.html',context) 
#    else:
#       print('Home False')
#       return redirect(f'/{usecase}')
   
def dna(request):
   usecase_q = Q(Q(usecase__icontains='DnA'))
   resp = Results.objects.filter(usecase_q).order_by('-upvote')
   if 'usecase_query' in request.GET:
      print("inside")
      q = request.GET['usecase_query']
      all_q = Q((Q(usecase__icontains='dna'))  & (Q(title__icontains=q) | Q(description__icontains=q)))
      resp = Results.objects.filter(all_q).order_by('-upvote')
   context = {
      'resp':resp
   }   
   return render(request, 'firstapp/usecase.html',context) 
   
def tech(request):
   usecase_q = Q(Q(usecase__icontains='Tech'))
   resp = Results.objects.filter(usecase_q).order_by('-upvote')
   if 'usecase_query' in request.GET:
      print("inside")
      q = request.GET['usecase_query']
      all_q = Q((Q(usecase__icontains='tech'))  & (Q(title__icontains=q) | Q(description__icontains=q)))
      resp = Results.objects.filter(all_q).order_by('-upvote')
   context = {
      'resp':resp
   }   
   return render(request, 'firstapp/usecase.html',context) 

def eng(request):
   print('Home True')
   usecase_q = Q(Q(usecase__icontains='Eng'))
   resp = Results.objects.filter(usecase_q).order_by('-upvote')
   if 'usecase_query' in request.GET:
      print("inside")
      q = request.GET['usecase_query']
      all_q = Q((Q(usecase__icontains='eng'))  & (Q(title__icontains=q) | Q(description__icontains=q)))
      resp = Results.objects.filter(all_q).order_by('-upvote')
   context = {
      'resp':resp
   }   
   return render(request, 'firstapp/usecase.html',context)  

def newcode(request):
      print("workinh")
      form = CodeForm()
      return render(request,"firstapp/uploadcode.html",{'form': form})
     
def uploadcode(request):
      print('Upload Code')
      if request.method== "POST":
           codeform = CodeForm(data=request.POST)
           if(codeform.is_valid()):
                codeform.save()
                text = f'''
                  Title: {request.POST['title']} ,
                  Description: {request.POST['description']},  
                  Code: {request.POST['usecase']} 
                '''
                add_to_vectorstore(text, 'Code')
                return redirect('/')
           else:
                return JsonResponse({'error': 'error'})

def updatecode(request,id):
      print('Update Code')
      getform = Results.objects.get(id=id)
      if request.method== "GET":
         form = CodeForm(instance=getform)
         context = {
             "form":form, 
             "id":id
             }
         return render(request,"firstapp/forms.html",context)
      
      if request.method== "POST":
         form = CodeForm(instance=getform, data=request.POST)
         form.save()
         context = {
            'resp':getform
         }
         return render(request,"firstapp/viewcode.html",context)

def viewcode(request,id):
      getform = Results.objects.get(id=id)
      getform.view_count=getform.view_count+1
      getform.save()
      context = {
      'resp':getform
   }
      return render(request,"firstapp/viewcode.html",context)

def upvote(request,id):

      getform = Results.objects.get(id=id)
      getform.upvote = getform.upvote+1
      getform.save()
      
      context = {
      'resp':getform
      }
      # return redirect(f'/viewcode/{id}')
      return JsonResponse({'upvote': getform.upvote})


def copycount(request,id):

      getform = Results.objects.get(id=id)
      getform.copy_count = getform.copy_count+1
      getform.save()
      
      context = {
      'resp':getform
      }
      # return redirect(f'/viewcode/{id}')
      return JsonResponse({'copy_count': getform.copy_count})

def advsearch(request):
    print('Adv Search')
    return render(request,"firstapp/advsearch.html")

import operator
from functools import reduce
def adv_searcher(request):
    str_1 = 'sample_str'
    output_str = retriever_bot(request.POST['query'][0], 3, 'Search', 'Code')['result']
    print(output_str)
    output_proc = output_str.split(', ')
    print(output_proc)
    #  title_q = Q(Q(title__icontains = output_proc[0])|Q(title__icontains = output_proc[1])|Q(title__icontains = output_proc[2]))
   #  title_q = reduce(operator.and_, (Q(title__icontains=x) for x in output_proc))
   #  resp = Results.objects.filter(title_q)
   #  title_q = Q(Q(title__icontains = 'Crypto Sync')|Q(title__icontains = 'Weather Sync using API')|Q(title__icontains = 'Weather Sync using API'))
    resp = Results.objects.filter(title__in=output_proc)

    context = { "resp": resp, "q" : request.POST['query']}

    return render(request,"firstapp/advsearch.html",context)

def simsearch(request):
    return render(request,"firstapp/simsearch.html")

def sim_search(request):
   inp= request.POST.get('param')
   out= run([sys.executable,'C:\\Users\\kartikey.gautam\\hackiq\\mquery\\faiss_test.py',inp],shell=False,stdout=PIPE)
   return render(request,'firstapp/simsearch.html',{'data1':out.stdout})


def gpt_explain_page(request):
    return render(request,"firstapp/gptexplain.html")

def gpt_explain(request):
    output_str = retriever_bot(request.POST['query'], 3, 'Technical', 'Schema')['result']
   #  output_str = '''To fetch audience data based on an impression, you can use the "LLD_user_id" attribute from the "LLD Impressions Feed" dataset and match it with the "LLD_user_id" attribute from the "Audience Data" dataset. This will give you the corresponding "segment_id" for the audience segment associated with that impression.'''
    context = { "data": output_str ,"q" : request.POST['query']}
    return render(request,"firstapp/gptexplain.html",context)

def ppt_explain_page(request):
    return render(request,"firstapp/chatppt.html")

def ppt_explain(request):
    str_1 = 'GPT response for PPT'
    context = { "data": str_1 ,"q" : request.POST.get('file_url','')}
    return render(request,"firstapp/chatppt.html",context)

def browseusecase(request):
    return render(request,"firstapp/browseusecase.html")

def scoreboard(request):
    ranks = Results.objects.order_by('-upvote','-copy_count','-view_count')[:5]
    context ={
        'resp':ranks
    }
    return render(request,"firstapp/scoreboard.html",context)
