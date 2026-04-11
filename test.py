import pandas as pd
import random

# -------- CONFIG --------
N = 500

# Locations with real coordinates
locations = [
    {"name": "Federation Square", "lat": -37.817979, "lon": 144.969057},
    {"name": "Flinders Street Station", "lat": -37.818271, "lon": 144.967061},
    {"name": "Queen Victoria Market", "lat": -37.8076, "lon": 144.9568},
    {"name": "St Kilda Beach", "lat": -37.8676, "lon": 144.9806},
    {"name": "Royal Botanic Gardens", "lat": -37.8304, "lon": 144.9796},
    {"name": "Melbourne Central", "lat": -37.8102, "lon": 144.9623},
    {"name": "Chapel Street", "lat": -37.8430, "lon": 144.9930},
    {"name": "Hosier Lane", "lat": -37.8163, "lon": 144.9690},
    {"name": "Southbank Promenade", "lat": -37.8206, "lon": 144.9653},
    {"name": "Carlton Gardens", "lat": -37.8060, "lon": 144.9717}
]

# Cultural + memory-focused templates
cultural_food = [
    "I remember sharing traditional food here with friends, it felt like a celebration of culture",
    "The mix of cultural cuisines here reminds me of Melbourne's diversity",
    "Tried a dish that reflected authentic heritage and family traditions",
    "The food here connects deeply to cultural roots and history",
    "Every meal here feels like experiencing a different culture"
]

memories = [
    "I used to come here as a child, it holds a lot of personal memories",
    "This place reminds me of family gatherings and special moments",
    "I have vivid memories of spending weekends here with loved ones",
    "Being here feels nostalgic, like revisiting an important part of my life",
    "This location has always been meaningful in my personal journey"
]

culture_general = [
    "You can really feel the cultural diversity and artistic energy here",
    "This place represents the multicultural identity of Melbourne",
    "There's a strong sense of community and cultural expression here",
    "Art, music, and people come together to create a cultural hub",
    "It's a place where different cultures blend seamlessly"
]

# -------- 20 NEW COMMENTS PER LOCATION --------
location_comments = {
    "Federation Square": [
        "The giant screens and open plaza make every event feel electric",
        "Watched a live broadcast here with thousands of strangers who felt like friends",
        "Federation Square is the beating heart of Melbourne's public life",
        "The architecture alone is worth the visit, bold and thought-provoking",
        "I love how this space welcomes everyone regardless of background",
        "Caught a free outdoor film screening here on a warm summer evening",
        "The galleries inside are hidden gems most tourists walk past",
        "It's hard to visit Melbourne and not end up at Fed Square at some point",
        "There's always something happening here, never a dull moment",
        "The Yarra River views from the edge of the square are stunning",
        "Met so many interesting people just sitting on the steps people-watching",
        "The ACMI museum here changed how I think about screen culture",
        "This is where Melbourne comes together to celebrate and grieve alike",
        "First night in Melbourne I wandered here and instantly felt welcome",
        "The square feels alive even on quiet weekday mornings",
        "Love the contrast between the edgy architecture and the classic Flinders church behind it",
        "Attended a cultural festival here that showcased over fifteen different communities",
        "The lighting at night transforms the whole space into something magical",
        "It feels like the city's living room and I always come back",
        "Saw a protest, a wedding photo shoot, and a busker all in one afternoon here"
    ],
    "Flinders Street Station": [
        "Meeting under the clocks is a Melbourne tradition I grew up with",
        "The golden facade of this station never gets old no matter how many times I see it",
        "Rushing through here during peak hour is chaotic but oddly thrilling",
        "This station has seen generations of Melburnians come and go",
        "The ballroom upstairs is a secret history most commuters never know about",
        "I proposed to my partner on the steps here, it felt right",
        "The heritage architecture makes every commute feel a little more grand",
        "Watched the NYE fireworks from the bridge right beside the station",
        "There's something deeply Melbourne about catching a train from Flinders Street",
        "The dome and arched windows glow beautifully in the late afternoon light",
        "Even as a daily commuter, I still appreciate how beautiful this building is",
        "The buskers here are some of the best musicians in the city",
        "Sitting on the steps watching the trams go by is a Melbourne ritual",
        "This station connects the whole city and carries so much history",
        "My grandparents met here in the 1960s, now it means everything to our family",
        "The station café has the best quick coffee before an early morning train",
        "First time I arrived by train from the airport, this was my welcome to the city",
        "The ornate entrance always makes me slow down and appreciate it",
        "Kids still press their noses against the glass looking at the train departures board",
        "A landmark that genuinely deserves its iconic status"
    ],
    "Queen Victoria Market": [
        "Nothing beats wandering through the deli hall on a Saturday morning",
        "The vendors here have been running their stalls for multiple generations",
        "Bought the freshest seasonal produce I've ever tasted at this market",
        "The night market in summer is a Melbourne highlight every single year",
        "This market carries the soul of Melbourne's migrant history",
        "The cheese and smallgoods section is dangerously good for my wallet",
        "Coming here early before the crowds feels like having the city to yourself",
        "My nonna used to bring me here every Sunday without fail",
        "The mix of fresh flowers, food, and clothing in one place is unbeatable",
        "You can taste cuisines from six different cultures in a single visit",
        "The market has resisted overdevelopment and kept its authentic character",
        "The noise, colour, and energy here is like nowhere else in Melbourne",
        "Picked up ingredients here and cooked the best meal of my year",
        "There's a warmth between the vendors and regulars that you can feel immediately",
        "The sheds have barely changed in a century and that's exactly how it should be",
        "Got talking to a spice vendor who told me stories about her home country for an hour",
        "The fresh juice stalls here are the perfect start to any morning",
        "This market is proof that Melbourne's cultural diversity is its greatest strength",
        "Walking through here feels like travelling the world without leaving the city",
        "My favourite ritual is grabbing a hot jam doughnut near the entrance"
    ],
    "St Kilda Beach": [
        "Watching the sun set over the bay from here is one of life's simple joys",
        "The penguins nesting at the end of the pier are an unexpected delight",
        "St Kilda has a gritty, artistic soul that the beach only adds to",
        "Sunday afternoons here with live music drifting from the esplanade feel perfect",
        "The palm-lined promenade has a relaxed energy unlike any other Melbourne suburb",
        "Luna Park watching over the beach gives the whole place a dreamlike quality",
        "Growing up, this beach was where summer truly began for our family",
        "The café strip on Acland Street after a swim is a ritual I never tire of",
        "Rollerblading along the foreshore on a clear winter morning is underrated",
        "This beach belongs to everyone in Melbourne equally, I love that about it",
        "The sunburned sailboats dotting the bay remind me of long childhood summers",
        "St Kilda has reinvented itself many times but the beach always anchors it",
        "Brought my visiting relatives here and they were genuinely blown away",
        "The smell of sea air mixed with coffee from the kiosks is iconic",
        "Watched a pod of dolphins from the pier which I still can't believe happened",
        "The graffiti and street art along the foreshore gives it a living gallery feel",
        "New Year's Day walk along this beach has become a personal tradition",
        "There's a timelessness here that survives every trend and redevelopment",
        "The beach volleyball regulars here make it feel like a neighbourhood community",
        "Best fish and chips in Melbourne eaten right here on the sand"
    ],
    "Royal Botanic Gardens": [
        "Walking through here is the fastest way to decompress after a stressful week",
        "The ornamental lake with black swans is one of Melbourne's most peaceful scenes",
        "Attended an outdoor cinema night here and it was absolutely magical",
        "The garden design feels like a curated journey through different ecosystems",
        "My favourite lunch spot in all of Melbourne is a quiet bench near the fern gully",
        "The ancient trees here make you feel small in the best possible way",
        "Spotted a ring-tailed possum on a low branch during an evening stroll",
        "The Indigenous plant walk taught me so much about Country and culture",
        "Proposed here during a morning walk and she said yes immediately",
        "These gardens are a living archive of botanical history and research",
        "Perfect place to bring a book and disappear from the city for an afternoon",
        "The café overlooks the lake and serves some of the best scones in town",
        "Families, joggers, tourists, and students all share this space beautifully",
        "The gardens at dusk when the light goes golden are genuinely breathtaking",
        "Every season brings something entirely different to look forward to here",
        "The cactus and succulent section is surprisingly fascinating",
        "Running the tan track that borders the gardens is a Melbourne rite of passage",
        "The gates open early and an early morning visit feels like private access",
        "Children's imagination runs wild here in a way that screens never can replicate",
        "This place reminds me that green space in a city is not a luxury but a necessity"
    ],
    "Melbourne Central": [
        "The giant shot tower preserved inside the atrium is an extraordinary piece of history",
        "This shopping centre managed to keep its heritage character while modernising",
        "The cone above the tower is one of Melbourne's most distinctive architectural features",
        "I come here more for the architecture than the shops honestly",
        "The food court represents Melbourne's multicultural food scene perfectly",
        "Rushing through the underground tunnel to catch a train is a daily adventure",
        "The cuckoo clock above the entrance is a quirky surprise for first-time visitors",
        "Melbourne Central feels like a city within the city",
        "Great spot to shelter from the rain and still feel like you're in the heart of the CBD",
        "The atrium floods with natural light in a way that makes the whole space feel open",
        "Meeting by the clock is the Melbourne Central version of the Flinders Street clocks",
        "The variety of independent retailers here alongside chains makes it feel curated",
        "I love that they built the shopping centre around the tower rather than demolishing it",
        "There are quiet corners on upper levels that most people rushing through never find",
        "The connection between the train station and the centre is genuinely seamless",
        "Spotted a live jazz performance in the atrium on a random Tuesday afternoon",
        "The history of this site layered on top of itself makes for fascinating reading",
        "Students from nearby universities fill this place with energy every weekday",
        "Night shopping here in December with all the festive decorations is genuinely fun",
        "The rooftop has views of the CBD that most visitors completely overlook"
    ],
    "Chapel Street": [
        "Chapel Street reinvents itself every few years but never loses its edge",
        "The vintage stores here are some of the best op shopping in Melbourne",
        "Found an incredible independent bookshop tucked between two bars here",
        "The brunch culture on this street is taken very seriously and deservedly so",
        "Street style watching on Chapel on a Saturday is better than any fashion magazine",
        "The stretch from Prahran to South Yarra each has its own distinct personality",
        "This street is where Melbourne's creative industries meet retail and nightlife",
        "Discovered my favourite clothing brand at a tiny independent store here",
        "The neighbourhood has gentrified but the bohemian energy still survives",
        "Spent an entire afternoon here just wandering without any particular destination",
        "The market at Prahran is a quieter, more local alternative to Queen Vic",
        "Nightlife here starts late and goes later, which suits Melbourne perfectly",
        "The food options have diversified enormously over the past decade",
        "Chapel Street is one of those places that always has something new to discover",
        "Caught a live DJ set spilling out of a bar onto the footpath one Friday evening",
        "The stretch near Commercial Road has amazing Middle Eastern restaurants",
        "There's an honest grit to parts of Chapel Street that keeps it feeling real",
        "My first apartment in Melbourne was a five minute walk from here",
        "The tram ride down Chapel Street is a Melbourne experience in itself",
        "Love how independent businesses here still hold their own against chain stores"
    ],
    "Hosier Lane": [
        "The street art here changes constantly and each visit feels completely new",
        "This laneway is proof that public space can be genuinely transformative art",
        "Watched an artist work on a mural here for hours, totally transfixed",
        "The cobblestones and layered walls give Hosier Lane a texture unlike anywhere else",
        "Brought an overseas friend here and they called it the most unique place they'd visited",
        "The work ranges from political commentary to pure beauty and everything in between",
        "There's an unwritten code of respect among the artists that keeps the space vibrant",
        "Photography here is a favourite hobby for Melburnians and tourists alike",
        "The laneways culture is what separates Melbourne from every other Australian city",
        "Came here on a weeknight and had the whole lane almost to myself",
        "The art is raw, confrontational, and deeply reflective of the city's mood",
        "Stumbled here on my first trip to Melbourne and it immediately became my favourite spot",
        "Watched a couple have their wedding photos taken against the murals, it worked perfectly",
        "The detail in some of these works rivals anything in a formal gallery",
        "Returned six months later and the entire lane had been repainted fresh",
        "Melbourne's laneway culture started here and radiates outward through the whole CBD",
        "There's a sense of democracy in street art that gallery culture can't always match",
        "Kids react to this art with more wonder than anything in a traditional museum",
        "The way natural light hits the walls at different times of day changes everything",
        "This lane has appeared in more Instagram feeds than almost any Melbourne landmark"
    ],
    "Southbank Promenade": [
        "The view of the CBD from the Southbank side of the Yarra is Melbourne at its best",
        "Walking here on a clear winter morning with a takeaway coffee is pure contentment",
        "The Arts Centre spire rising above the promenade makes for a perfect skyline",
        "Saturday evening crowds here have a relaxed festive energy that's hard not to love",
        "The restaurants lining the promenade are overpriced but the location compensates",
        "Watched the Moomba fireworks from here and it was spectacular",
        "Southbank has transformed from an industrial wasteland to Melbourne's cultural spine",
        "The pedestrian bridges give you different angles of the city at every turn",
        "This is where Melbourne comes to celebrate on New Year's Eve without fail",
        "The mix of high-end dining, buskers, and families feels inclusive and right",
        "Running along the promenade in the early morning when it's quiet is meditative",
        "Caught a street performer here who held a crowd of two hundred people spellbound",
        "The Crown end of Southbank has a very different energy to the Arts Centre end",
        "Love watching the tourist boats move slowly up the Yarra from a bench here",
        "The reflections of the city lights in the river at night are breathtaking",
        "This promenade connects Melbourne's arts, food, and natural environment seamlessly",
        "Every weekend market along here discovers a new way to bring people together",
        "Brought my parents here from interstate and they finally understood why I love Melbourne",
        "The boardwalk sections over the water give you a sense of floating through the city",
        "Southbank in summer is alive in a way that only water frontages can manage"
    ],
    "Carlton Gardens": [
        "The Museum of Melbourne sitting inside these gardens is a brilliant combination",
        "The heritage fountain at the centre of the gardens is a beautiful focal point",
        "Carlton Gardens has a more formal, European feel than most Melbourne parks",
        "This is where Melburnians come to sit with a book and completely disappear",
        "The elm trees lining the paths create incredible cathedral-like canopies in autumn",
        "Morning tai chi groups here give the gardens a quietly multicultural rhythm",
        "The gardens are on the World Heritage list which still surprises many locals",
        "Children running between the trees while parents rest on benches, a timeless scene",
        "The exhibition building in the gardens is one of Australia's most significant structures",
        "Visiting during the Melbourne International Flower and Garden Show is spectacular",
        "The lawns here are genuinely immaculate, someone cares deeply about this space",
        "This park marks the northern edge of the CBD and signals a change in pace",
        "Cycling through these gardens on my way to work is the best part of my commute",
        "The light through the elms on a late afternoon in March is extraordinarily beautiful",
        "The gardens feel underrated compared to the Botanic Gardens but deserve equal love",
        "Watching the Museum light up at night from within the dark gardens is wonderful",
        "The Carlton community uses this park as their living room and it shows",
        "Found a very old tortoise living in the garden beds that no one else seemed to notice",
        "The heritage protections here mean this space will exist for future generations to enjoy",
        "A perfectly preserved Victorian garden in the middle of a modern city is a rare gift"
    ]
}

# Combine all comment pools
comment_pool = cultural_food + memories + culture_general

# -------- GENERATE DATA --------
data = []

for _ in range(N):
    loc = random.choice(locations)
    year = random.randint(2023, 2026)

    # Pick from location-specific comments OR the general pool
    loc_specific = location_comments.get(loc["name"], [])
    all_comments = comment_pool + loc_specific
    comment = random.choice(all_comments)

    likes = random.randint(0, 1000)

    data.append({
        "latitude": loc["lat"],
        "longitude": loc["lon"],
        "year": year,
        "comment_message": comment,
        "likes": likes
    })

# -------- CREATE DATAFRAME --------
df = pd.DataFrame(data)

# -------- SORT by (latitude, longitude) group, descending likes --------
df = (
    df.sort_values(["latitude", "longitude", "likes"], ascending=[True, True, False])
      .reset_index(drop=True)
)

# -------- SAVE CSV --------
df.to_csv("melbourne_cultural_dataset.csv", index=False)

print(df.head(20))
print(f"\nGenerated {len(df)} rows.")