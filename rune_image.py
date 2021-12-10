from PIL import Image
import requests
from io import BytesIO

def makeSection(bg, runeSection, num, sWidth, mult, add, y):
        for i in range(0, num): 
            if y == 472: 
                response = requests.get("https:" + runeSection[2][i])
            else: 
                response = requests.get("https:" + runeSection[i + (1 if y == 256 else 0)][1])
            image = Image.open(BytesIO(response.content))
            if image.width != sWidth: image.thumbnail((sWidth, sWidth)) # check
            bg.paste(image, (mult * (i + (1 if num == 1 else 0)) + add, y))

def makeImage(runes):
    width, height = 108*3*4+160, 256+108+108+48
    nImage = Image.new('RGBA', (width, height))
    for rune, n in zip(runes, range(0, len(runes))):
        # primary
        makeSection(nImage, rune[0][1], 1, 256, 34 , 0 + (364 * n), 0)
        makeSection(nImage, rune[0][1], 3, 108, 108 , 0 + (364 * n), 256)
        # secondary
        makeSection(nImage, rune[1][1], 2, 108, 108 , 54 + (364 * n), 364)
        # shards
        makeSection(nImage, rune, 3, 48, 48 , 90 + (364 * n), 472)

    return nImage

# paramlist = [[nImage, rune[0][1], 1, 256, 34 , 0 + (364 * n), 0],
#         [nImage, rune[0][1], 3, 108, 108 , 0 + (364 * n), 256],
#         [nImage, rune[1][1], 2, 108, 108 , 54 + (364 * n), 364],
#         [nImage, rune, 3, 48, 48 , 90 + (364 * n), 472]]


# # prtime = time.time()
# with concurrent.futures.ProcessPoolExecutor(1) as executor:
#     executor.map(makeSection, paramlist)