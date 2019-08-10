from django.shortcuts import render
import requests,json
# Create your views here.

'''
        SIGUN_CD	시군코드
        SIGUN_NM	시군명
        CMPNM_NM	상호명
        INDUTYPE_CD	업종코드
        BIZCOND_NM	업태명
        INDUTYPE_NM	업종명(종목명)
        REFINE_ROADNM_ADDR	소재지도로명주소
        REFINE_LOTNO_ADDR	소재지지번주소
        TELNO	전화번호
        REGION_MNY_NM	사용가능한지역화폐명
        BRNHSTRM_MNY_USE_POSBL_YN	지류형지역화폐사용가능여부
        CARD_MNY_USE_POSBL_YN	카드형지역화폐사용가능여부
        MOBILE_MNY_USE_POSBL_YN	모바일형지역화폐사용가능여부
        REFINE_ZIP_CD	우편번호
        REFINE_WGS84_LAT	위도
        REFINE_WGS84_LOGT	경도
        DATA_STD_DE	데이터기준일자

'''
def getdata(시군코드): 

    # 참고) 인천시 n번째 상호명 찾기 >> getdata("인천시")[n]['CMPNM_NM'] 


    url = "https://openapi.gg.go.kr/RegionMnyFacltStus?KEY=bf309b70d95a437bbf0693dab21778d3&Type=json"
    if 시군코드!="":
        url+= "&SIGUN_NM="+시군코드
    get_json = requests.get(url)
    _list = json.loads(get_json.text)
    _list = _list['RegionMnyFacltStus'][1]['row']
    return _list

def contact(request):
    return render(request,"contact.html")

def search(data,method,text): 
    # search(가져온 데이터, 찾는 상호명)
    # 참고) 인천시에서 국밥집 찾기 >> search(getdata("인천시"),"국밥")
    _list = [] 
    for dicts in data:
        if text in dicts[method]:
            _list.append(dicts)
    return _list


def hello(request):
    return render(request,'hello.html')
def about(request):
    for_list = []
    for_map = []
    hongkong = False
    if request.method=="POST":
        if ('dong' in request.POST and 'category' in request.POST):
            result = getdata("시흥시")
            if request.POST['dong'] != "전체":
                result = search(result,"REFINE_LOTNO_ADDR",str(request.POST['dong']))
            if request.POST['category']!="전체":
                result = search(result,"BIZCOND_NM",str(request.POST['category']))
            for items in result:
                for_list.append([str(items['CMPNM_NM']),str(items['REFINE_LOTNO_ADDR']),str(items['REFINE_WGS84_LAT'])+"_"+str(items['REFINE_WGS84_LOGT'])])
            for items in result:
                for_map.append([items['REFINE_WGS84_LAT'],items['REFINE_WGS84_LOGT']])

        elif 'caviarSearch' in request.POST:
            result = getdata("시흥시")
            result = search(result,"CMPNM_NM",str(request.POST['caviarSearch']))
            for items in result:
                for_list.append([str(items['CMPNM_NM']),str(items['REFINE_LOTNO_ADDR']),str(items['REFINE_WGS84_LAT'])+"_"+str(items['REFINE_WGS84_LOGT'])])
            for items in result:
                for_map.append([items['REFINE_WGS84_LAT'],items['REFINE_WGS84_LOGT']])
    if len(for_list)>0:
        return render(request,"about.html",{'list':for_list,'locx': for_map[0][0],'locy': for_map[0][1],'le': range(1,len(for_list)+1),'hongkong':hongkong})
    else:
        hongkong = True
        return render(request,"about.html",{'list':for_list,'locx': 37.474056,'locy': 126.9833588,'le': range(0),'hongkong':hongkong})