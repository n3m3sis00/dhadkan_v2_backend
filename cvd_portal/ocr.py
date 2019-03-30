import sys
import requests
import cv2


def ocr_space_file(filename, overlay=False, api_key='helloworld', language='eng'):


    payload = {'isOverlayRequired': overlay,
               'apikey': '3047397b1388957',
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.json()

test_file = ocr_space_file(filename=sys.argv[1], language='eng',overlay=True)


final_dict = []



for i in test_file['ParsedResults'][0]['TextOverlay']['Lines']:
    if len(i["Words"][0]) == 1:
        final_dict.append(i["Words"][0])

    else:
        for j in i["Words"]:
            final_dict.append(j)



img = cv2.imread(sys.argv[1])
font = cv2.FONT_HERSHEY_SIMPLEX
for i in range(len(final_dict)):
    cv2.rectangle(img, (int(final_dict[i]['Left']), int(final_dict[i]['Top'])), (int(final_dict[i]['Left']+final_dict[i]['Width']), int(final_dict[i]['Top']+final_dict[i]['Height'])), (255,20,0), 2)
    cv2.putText(img,final_dict[i]["WordText"],(int(final_dict[i]['Left']),int(final_dict[i]['Top'])), font, 1,(255,0,255),2,cv2.LINE_AA)


cv2.imshow('OCR Output',img)
cv2.waitKey(0)
print(test_file)
print(len(test_file['ParsedResults'][0]['TextOverlay']))
print(final_dict[0])
