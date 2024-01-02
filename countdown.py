# %%
import drawsvg as draw
import numpy as np


def add_trailing_zeros(num):
    if num < 10:
        return f"0{num}"
    else:
        return str(num)


def hideSqureDots(x, y, sec, min):
    c = draw.Rectangle(0, 5, 10, 10, fill='#000000')
    c.append_anim(
        draw.Animate(
            'y',
            '0s',
            '{}'.format(y),
            '{}'.format(y),
            '{}s'.format(min*sec+1),
            repeatCount='indefinite'
        )
    )

    c.append_anim(draw.Animate('x', '0s', '{}'.format(x), '{}'.format(x), '{}s'.format(min*sec+1), repeatCount='indefinite'))
    c.append_anim(draw.Animate('fill', '{}s'.format(0), '#000000', 'white', '{}s'.format(min*sec+1), repeatCount='indefinite'))
    return c


def drawBlackDot(rect, xRect, yRect, timerL):
    sqDot = draw.Rectangle(0, 0, 10, 10, fill='black')
    sqDot.add_key_frame(0, x=xRect, y=yRect, width=0, height=0)
    sqDot.add_key_frame((rect+1)*timerL, x=xRect, y=yRect, width=0, height=0)
    sqDot.add_key_frame((rect+1)*timerL, x=xRect, y=yRect, width=10, height=10)
    return sqDot


add_trailing_zeros_vec = np.vectorize(add_trailing_zeros)

fntStyle = "font-size:150px;font-family:'Retro Gaming';fill:#e7e514;"

totalTimerLength = 15  # min
sqWidth = 800
sqHeight = 400

d = draw.Drawing(
        sqWidth,
        sqHeight,
        origin='center',
        animation_config=draw.types.SyncedAnimationConfig(
            # Animation configuration
            duration=totalTimerLength*60+1,
            repeat_count=0  # Seconds
            # show_playback_progress=True,
            # show_playback_controls=True
        )
    )

# Draw a rectangle
r = draw.Rectangle(sqWidth/-2, sqHeight/-2, sqWidth, sqHeight, fill='#000000')
d.append(r)

r = draw.Rectangle(sqWidth/-2+20, sqHeight/-2+20, sqWidth-35, sqHeight-40, fill='#00000000', stroke='#1d21c5', stroke_width=2)
d.append(r)

r = draw.Rectangle(sqWidth/-2+50, sqHeight/-2+50, sqWidth-95, sqHeight-100, fill='#00000000', stroke='#1d21c5', stroke_width=2)
d.append(r)

npSec = np.arange(0, totalTimerLength*60+1, 1)
npSecStr00 = np.array(['00'])
npSecStr59 = np.arange(59, 0, -1)
npSecStr59 = add_trailing_zeros_vec(npSecStr59)
npSecStr60 = np.append(npSecStr00, npSecStr59)

npSecStr = np.array([])
for cntMin in range(totalTimerLength):
    npSecStr = np.append(npSecStr, npSecStr60)

npSecStr = np.append(npSecStr, np.array(['00']))

npMin = np.arange(1, (totalTimerLength)*60, 60)
npMin = np.append(np.array([0]), npMin)
npMinStr = np.arange(totalTimerLength, -1, -1)
npMinStr = add_trailing_zeros_vec(npMinStr)

# Static text
d.append(draw.Text(':', 0, 0, 0, style="font-size:150px;font-family:'Retro Gaming';fill:#e7e514;", center=True))

# Changing text
# Minutes
draw.native_animation.animate_text_sequence(
        d,
        npMin,
        npMinStr,
        0, -140, 0, style="font-size:150px;font-family:'Retro Gaming';fill:#e7e514;", center=True)

# Seconds
draw.native_animation.animate_text_sequence(
        d,
        npSec,
        npSecStr,
        0, 140, 0, style="font-size:150px;font-family:'Retro Gaming';fill:#e7e514;", center=True)

# draw.native_animation.animate_element_sequence()

dist = 35
topDots = 22  # 44
sideDots = 8  # 16
totalDots = topDots*2+sideDots*2
xRect = -370
yRect = 150
rect = 0
sqDot = drawBlackDot(rect, xRect, yRect, totalTimerLength)

for rect in range(61):

    if rect > topDots*2+sideDots:
        # Left side 
        xRect = -370
        yRect = 150-(rect-topDots*2-sideDots)*dist
        sqDot = drawBlackDot(rect, xRect, yRect, totalTimerLength)
        # print(rect, xRect, yRect)
    elif rect > topDots+sideDots:
        # Bottom
        xRect = 435-(rect-topDots-sideDots+1)*dist
        yRect = 160
        sqDot = drawBlackDot(rect, xRect, yRect, totalTimerLength)
        # print(rect, xRect, yRect, topDots, sideDots, dist)
    elif rect > topDots:
        # Right side
        xRect = -440+(topDots+1)*dist
        yRect = -165+(rect-topDots)*dist
        sqDot = drawBlackDot(rect, xRect, yRect, totalTimerLength)
        # print(rect, xRect, yRect)
    elif rect <= topDots and rect > 0:
        # Top
        xRect = -405+rect*dist
        yRect = -170
        sqDot = drawBlackDot(rect, xRect, yRect, totalTimerLength)

    elif rect == 0:
        xRect = -500
        yRect = -300

    r = draw.Rectangle(xRect, yRect, 10, 10, fill='white')  # Moving square
    d.append(r)

    # c = hideSqureDots(xRect, yRect, rect, totalTimerLength)
    # d.append(c)

    d.append(sqDot)

# for i in range(61):
#     sqDot = draw.Rectangle(0, 0, 10, 10, fill='black')
#     sqDot.add_key_frame(0, x=-405+dist, y=-170, width=10, height=10)
#     sqDot.add_key_frame(i+1, x=-405+dist*(i+2), y=-170, width=10, height=10)
#     d.append(sqDot)

# Animation
# kf1 = ((topDots+1)/totalDots)*(totalTimerLength*60)
# kf2 = ((sideDots)/totalDots)*(totalTimerLength*60)+kf1
# kf3 = (topDots/totalDots)*(totalTimerLength*60) + kf2
# kf4 = ((sideDots)/totalDots)*(totalTimerLength*60)+kf3

# circleRadius = 10
# circle = draw.Circle(0, 0, 0, fill='orange')  # Moving circle
# circle.add_key_frame(0, cx=-400+circleRadius+20, cy=-200+circleRadius+26, r=circleRadius)
# circle.add_key_frame(kf1, cx=400-circleRadius-20, cy=-200+circleRadius+26, r=circleRadius)
# circle.add_key_frame(kf2, cx=400-circleRadius-20, cy=200-circleRadius-26, r=circleRadius)
# circle.add_key_frame(kf3, cx=-400+circleRadius+25, cy=200-circleRadius-26, r=circleRadius)
# circle.add_key_frame(kf4, cx=-400+circleRadius+25, cy=-200+circleRadius+26, r=circleRadius)
# d.append(circle)

# p = draw.Path(fill='blue')
# p.arc(0, 0, 51, 20, -20, cw=False)
# p.arc(0, 0, 20, 20, -20, cw=True, include_l=True)
# p.Z()

# p.add_key_frame(0, cx=0, cy=0, r=circleRadius, start_deg=20, end_deg=-20, cw=True, include_l=True)
# p.add_key_frame(2, cx=100, cy=0, r=circleRadius, start_deg=20, end_deg=-20, cw=True, include_l=True)

# d.append(p)

# ----------------------------------------------------------------------------
# Save as a standalone animated SVG or HTML
d.save_mp4(
    'retrogameCountdownTimer_{}min.mp4'.format(totalTimerLength),
    fps=1, verbose=True
)

# d.save_svg('counter.svg')
# d.save_html('conter.html')
# d.display_inline()  # Display as interactive SVG
