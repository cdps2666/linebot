import os
import json
import re
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def get_travel_plan(video_context):
    
    # os.environ["OPENAI_API_KEY"] = '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'
    # text-davinci-003
    
    llm = OpenAI(openai_api_key="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",max_tokens=1024,temperature=0.3)
    dict =  {'order': 1, 'location': '地點名稱'}

    # prompt
    dict_str = json.dumps(dict, ensure_ascii=False)
    prompt = PromptTemplate(
        input_variables=["context","dict"],
        template="根據以下的旅遊影片文字稿，摘列點行程，並依照[{dict}]格式輸出array結果，不輸出其內容.\n文字稿:{context}"
    )

    # chain
    chain = LLMChain(llm=llm, prompt=prompt)
    print(prompt.format(dict=dict_str,context=video_context))

    # execution
    travel_plan = []
    input_string = ''
    # input_string = '''
    # [{"order": 1, "location": "渭水之丘"},
    # {"order": 2, "location": "張美阿嬤農場"},
    # {"order": 3, "location": "清水地熱公園"},
    # {"order": 4, "location": "北門綠豆沙牛乳大王"},
    # {"order": 5, "location": "猴洞坑瀑布"},
    # {"order": 6, "location": "龜山島日出海灘"},
    # {"order": 7, "location": "蘭陽博物館"},
    # {"order": 8, "location": "梅花湖"},
    # {"order": 9, "location": "金車噶瑪蘭威士忌酒廠"},
    # {"order": 10, "location": "蘭城晶英的紅樓中餐廳"}]
    # '''
    input_string = chain.run({'dict': dict_str,'context': video_context})
    try:
        travel_plan = json.loads(input_string)

    except Exception as e:

        try:
            match = re.search(r'\[.*\]', input_string)
            json_string = match.group()

            travel_plan = json.loads(json_string)
            print(travel_plan)
        except Exception as e:
            print(f"Chat GPT 結果轉json失敗：{e}")

    return travel_plan


if __name__ == "__main__":

    video_context=f"春日東北季風稍歇、雨勢稍緩 ,遊玩九份一帶是最適合的季節,J編也要幫親子開發九份的最新玩法,第1站先來到金瓜石的黃金博物館,這裡保留從30年代開始的採礦過往,日式的古蹟群是歷史的遺跡,鐵道和車站是淘金的證據 ,淘金體驗是親子必玩,選定覺得最有緣分的河沙後,就可以跟著導覽老師的指示 ,開始運用各種物質的比重不同,以及離心力方式將沙和金分離 ,體驗歷史過程也來堂自然課,經歷千辛萬苦才能把金帶回家,另一個更有臨場感的就是坑道體驗啦,挑選好適合的安全裝備後,就能進入當年礦工真正的工作場域,窄暗濕的通道內了解礦工的艱辛,透過模型還原各種場景 ,搭配多媒體裝置的輔助 ,讓體驗更身歷其境,接著就往下一站前進啦 ,山城美館就在金瓜石山腳下,這裡展示在地的文創作品,可愛的模樣大小朋友都會很愛,最酷的是展場內還有QRcode,透過AR技術創造小彩蛋,館內另有座位區提供DIY,跟孩子選一種自己喜歡的吧,<離開前別忘了走到戶外 ,看看陰陽海和十三層選鍊場遺址,肚子餓就回到九份老街吃小吃吧,魚丸伯仔是在地70年老店,販售品項相當單純 ,魚丸湯口感Q彈喝了暖胃,豆干包像阿給和魚丸的綜合體,不想錯過經典芋圓就吃賴阿婆吧 ,座椅是可愛的瓶蓋,芋園有5種口味並採現煮,配上甜湯實在太幸福,夜晚就在九份山城漫步吧,自己逛或跟導覽都很適合,必訪點一是昇平戲院,老電影院在夜間有不同魅力,第二站可以欣賞知名的阿妹茶樓,從海悅樓前望過去是最美角度,最後就到金山岩眺望下方漁村之美吧,走累了就到石埤23補充能量吧,這裡是山城裡的深夜食堂,手作蔓越莓厚度超誇張,法式吐司配焦糖小朋友一定愛,春日的一日遊該去哪玩？,透過九份新玩法感受山城之美吧"
    
    # get_summary(video_context)
    result = get_travel_plan(video_context)

    print(result)
