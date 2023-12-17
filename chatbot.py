import re
import json


def extract_urls(text):
    # 定義簡單的正規表達式模式，以匹配簡單的URL格式
    url_pattern = re.compile(r'https?://\S+')

    # 使用 findall 方法找到所有匹配的網址
    urls = re.findall(url_pattern, text)

    return urls

def get_map_url(video_url):

    obj = {
        "url": "https://tinyurl.com/yssopd74",
        "location_list": [ 
            {'order':1,'location':'地點名稱','url':'https://tinyurl.com/yl64yqu9'},
            {'order':2,'location':'地點名稱','url':'https://tinyurl.com/yl64yqu9'}  
        ],
        "status":True
    }

    return obj

def get_response(input_message):
    msgs =[]

    result_urls = extract_urls(input_message)
    if len(result_urls) >0 :
        result = get_map_url(result_urls[0])
        if ( result ) :
            if( result['status'] == True) :
                url = result['url']
                msg = f"💡 根據您提供的影片，為您分析整理的旅遊行程:\n{url}"
                msgs.append(msg)

                msg = "\n⭐ 並列出以下各景點的位置\n"
                for item in result['location_list']:
                    order = item['order']
                    item_location = item['location']
                    item_url= item['url']
                    msg += f"{order}. {item_location} {item_url}\n"
                msgs.append(msg)
            else :
                msg ="🙇 很抱歉，出了點問題，無法為您分析旅遊行程，可以試試看別的影片。"
                msgs.append(msg)

    return  "\n".join(msgs)


if __name__ == "__main__":

    msg = get_response("https://www.youtube.com/watch?v=0exeq7-rZZc")
    print(msg)
        
