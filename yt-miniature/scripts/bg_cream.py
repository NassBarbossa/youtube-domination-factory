"""Convergence cream studio background 1280x720: cream, fine grid, warm halos behind each person, vignette."""
from PIL import Image, ImageDraw, ImageFilter
import sys
W,H=1280,720; S=2
out=sys.argv[1] if len(sys.argv)>1 else 'bg-cream.jpg'
img=Image.new('RGB',(W*S,H*S),(242,239,232))
d=ImageDraw.Draw(img)
for x in range(0,W*S,52*S): d.line([(x,0),(x,H*S)],fill=(230,225,214),width=S)
for y in range(0,H*S,52*S): d.line([(0,y),(W*S,y)],fill=(230,225,214),width=S)
# warm halos behind the two persons + slightly darker edges
halo=Image.new('RGB',(W*S,H*S),(0,0,0)); hd=ImageDraw.Draw(halo)
for cx,col in ((300,(255,220,160)),(980,(190,235,210))):
    hd.ellipse([cx*S-300*S,H*S-520*S,cx*S+300*S,H*S+200*S],fill=col)
halo=halo.filter(ImageFilter.GaussianBlur(120*S))
img=Image.blend(img,Image.composite(halo,img,halo.convert('L').point(lambda v:min(255,v))),0.35)
vig=Image.new('L',(W*S,H*S),0); vd=ImageDraw.Draw(vig); vd.ellipse([-200*S,-250*S,W*S+200*S,H*S+250*S],fill=255)
vig=vig.filter(ImageFilter.GaussianBlur(160*S))
dark=Image.new('RGB',(W*S,H*S),(214,208,196))
img=Image.composite(img,dark,vig)
img=img.resize((W,H),Image.LANCZOS); img.save(out,quality=94); print(out)
