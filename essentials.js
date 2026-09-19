/* 한글 Quest — Essentials: the survival vocabulary, sorted by job.
   Always open, never locked, no order to follow. A child can dip in on the plane.

   Organised the way a phrasebook should be: what each word DOES in a sentence.
   Rows are [ko, romanisation, english, emoji?, note?].                            */
(function () {
  const W = rows => rows.map(r => ({ ko: r[0], rom: r[1], en: r[2], emoji: r[3] || '💬', note: r[4] || '' }));

  const groups = [
    /* ================= 1. THE CORE BUILDING BLOCKS ================= */
    { id: 'core', title: 'The Core Building Blocks', sub: 'Action & identity', emoji: '🧱', icon: 'ess-core',
      blurb: 'The words that carry the meaning. Nothing happens in a sentence without these.',
      sections: [

        { id: 'v1', title: 'The ten verbs you cannot live without', kind: 'Verbs', emoji: '⚡', icon: 'ess-verbs',
          note: 'If you learn nothing else, learn these. Almost any sentence you need on the trip uses one of them.',
          words: W([
            ['이에요', 'ieyo', 'is / am / are', '🟰', 'After a consonant. 예요 after a vowel.'],
            ['있어요', 'isseoyo', 'there is / I have', '✅'],
            ['없어요', 'eopseoyo', "there isn't / I don't have", '❌'],
            ['해요', 'haeyo', 'do', '🔧'],
            ['가요', 'gayo', 'go', '🚶'],
            ['와요', 'wayo', 'come', '👉'],
            ['먹어요', 'meogeoyo', 'eat', '🍚'],
            ['마셔요', 'masyeoyo', 'drink', '🥤'],
            ['봐요', 'bwayo', 'see / watch / read', '👀'],
            ['주세요', 'juseyo', 'please give me', '🤲', 'Put any noun in front: 물 주세요.'],
            ['필요해요', 'piryohaeyo', 'need', '🆘'],
            ['원해요', 'wonhaeyo', 'want (a thing)', '🙏'],
            ['하고 싶어요', 'hago sipeoyo', 'want to do', '💭'],
            ['할 수 있어요', 'hal su isseoyo', 'can do', '💪'],
            ['못 해요', 'mot haeyo', "can't do", '🚫'],
            ['알아요', 'arayo', 'know', '💡'],
            ['몰라요', 'mollayo', "don't know", '🤷']
          ]) },

        { id: 'v2', title: 'The next fifteen verbs', kind: 'Verbs', emoji: '🏃', icon: 'ess-verbs2',
          note: 'Once the first ten are automatic, these carry almost everything else a child needs to say.',
          words: W([
            ['말해요', 'malhaeyo', 'say / speak', '💬'],
            ['들어요', 'deureoyo', 'hear / listen', '👂'],
            ['읽어요', 'ilgeoyo', 'read', '📖'],
            ['써요', 'sseoyo', 'write / use', '✍️'],
            ['사요', 'sayo', 'buy', '🛒'],
            ['찾아요', 'chajayo', 'look for / find', '🔎'],
            ['기다려요', 'gidaryeoyo', 'wait', '⏳'],
            ['도와줘요', 'dowajwoyo', 'help', '🤝'],
            ['열어요', 'yeoreoyo', 'open', '🚪'],
            ['닫아요', 'dadayo', 'close', '🔒'],
            ['타요', 'tayo', 'ride / get on', '🚌'],
            ['내려요', 'naeryeoyo', 'get off', '⬇️'],
            ['자요', 'jayo', 'sleep', '😴'],
            ['일어나요', 'ireonayo', 'get up', '🌅'],
            ['줘요', 'jwoyo', 'give', '🎁'],
            ['받아요', 'badayo', 'receive', '📬'],
            ['좋아해요', 'joahaeyo', 'like', '💖']
          ]) },

        { id: 'n1', title: 'People', kind: 'Nouns', emoji: '👨‍👩‍👧', icon: 'ess-people',
          note: 'Who you are talking about, or shouting for.',
          words: W([
            ['사람', 'saram', 'person', '🧍'],
            ['친구', 'chingu', 'friend', '🧑‍🤝‍🧑'],
            ['가족', 'gajok', 'family', '👨‍👩‍👧'],
            ['엄마', 'eomma', 'mum', '👩'],
            ['아빠', 'appa', 'dad', '👨'],
            ['동생', 'dongsaeng', 'younger brother or sister', '🧒'],
            ['할머니', 'halmeoni', 'grandmother', '👵'],
            ['할아버지', 'harabeoji', 'grandfather', '👴'],
            ['선생님', 'seonsaengnim', 'teacher', '🧑‍🏫'],
            ['학생', 'haksaeng', 'student', '🎒'],
            ['아이', 'ai', 'child', '🧒'],
            ['어른', 'eoreun', 'grown-up', '🧑'],
            ['아저씨', 'ajeossi', 'mister (a grown man)', '👨‍💼'],
            ['아주머니', 'ajumeoni', 'ma’am (a grown woman)', '👩‍💼'],
            ['의사', 'uisa', 'doctor', '🩺'],
            ['경찰', 'gyeongchal', 'police officer', '👮'],
            ['직원', 'jigwon', 'staff member', '🧑‍💼']
          ]) },

        { id: 'n2', title: 'Places you actually need', kind: 'Nouns', emoji: '📍', icon: 'ess-places',
          note: 'The ones worth knowing before you land.',
          words: W([
            ['화장실', 'hwajangsil', 'toilet', '🚻', 'The single most useful noun on this page.'],
            ['호텔', 'hotel', 'hotel', '🏨'],
            ['역', 'yeok', 'station', '🚉'],
            ['공항', 'gonghang', 'airport', '✈️'],
            ['병원', 'byeongwon', 'hospital', '🏥'],
            ['약국', 'yakguk', 'pharmacy', '💊'],
            ['가게', 'gage', 'shop', '🏪'],
            ['식당', 'sikdang', 'restaurant', '🍽️'],
            ['학교', 'hakgyo', 'school', '🏫'],
            ['집', 'jip', 'home / house', '🏠'],
            ['방', 'bang', 'room', '🚪'],
            ['공원', 'gongwon', 'park', '🌳'],
            ['은행', 'eunhaeng', 'bank', '🏦'],
            ['시장', 'sijang', 'market', '🧺'],
            ['버스 정류장', 'beoseu jeongnyujang', 'bus stop', '🚏'],
            ['출구', 'chulgu', 'exit', '🚪'],
            ['입구', 'ipgu', 'entrance', '🚪']
          ]) },

        { id: 'n3', title: 'Food and drink', kind: 'Nouns', emoji: '🍜', icon: 'ess-food',
          note: 'Enough to order a meal and stay fed for two weeks.',
          words: W([
            ['물', 'mul', 'water', '💧'],
            ['밥', 'bap', 'rice / a meal', '🍚'],
            ['빵', 'ppang', 'bread', '🍞'],
            ['고기', 'gogi', 'meat', '🥩'],
            ['생선', 'saengseon', 'fish (food)', '🐟'],
            ['계란', 'gyeran', 'egg', '🥚'],
            ['과일', 'gwail', 'fruit', '🍎'],
            ['채소', 'chaeso', 'vegetables', '🥬'],
            ['우유', 'uyu', 'milk', '🥛'],
            ['주스', 'juseu', 'juice', '🧃'],
            ['김치', 'gimchi', 'kimchi', '🌶️'],
            ['국', 'guk', 'soup', '🍲'],
            ['면', 'myeon', 'noodles', '🍜'],
            ['간식', 'gansik', 'a snack', '🍡'],
            ['설탕', 'seoltang', 'sugar', '🍬'],
            ['소금', 'sogeum', 'salt', '🧂'],
            ['얼음', 'eoreum', 'ice', '🧊']
          ]) },

        { id: 'n4', title: 'Things, money and emergencies', kind: 'Nouns', emoji: '🆘', icon: 'ess-things',
          note: 'The nouns you hope not to need, and the ones you will need every day.',
          words: W([
            ['돈', 'don', 'money', '💰'],
            ['카드', 'kadeu', 'card', '💳'],
            ['여권', 'yeogwon', 'passport', '🛂'],
            ['표', 'pyo', 'ticket', '🎫'],
            ['가방', 'gabang', 'bag', '🎒'],
            ['휴대폰', 'hyudaepon', 'mobile phone', '📱'],
            ['열쇠', 'yeolsoe', 'key', '🔑'],
            ['약', 'yak', 'medicine', '💊'],
            ['옷', 'ot', 'clothes', '👕'],
            ['신발', 'sinbal', 'shoes', '👟'],
            ['우산', 'usan', 'umbrella', '☂️'],
            ['이름', 'ireum', 'name', '🏷️'],
            ['주소', 'juso', 'address', '📮'],
            ['시간', 'sigan', 'time', '🕐'],
            ['길', 'gil', 'road / the way', '🛣️'],
            ['도움', 'doum', 'help', '🆘'],
            ['사고', 'sago', 'an accident', '🚨']
          ]) },

        { id: 'p1', title: 'Pronouns', kind: 'Pronouns', emoji: '🙋', icon: 'ess-pronouns',
          note: 'Korean drops these constantly — but you still need to recognise them, and to use them when it matters.',
          words: W([
            ['저', 'jeo', 'I / me (polite)', '🙇'],
            ['나', 'na', 'I / me (casual)', '🙋'],
            ['제', 'je', 'my (polite)', '🔖', '제 이름 = my name.'],
            ['내', 'nae', 'my (casual)', '🏷️'],
            ['너', 'neo', 'you (to a friend)', '👉'],
            ['우리', 'uri', 'we / our', '👨‍👩‍👧'],
            ['저희', 'jeohui', 'we / our (polite)', '👥'],
            ['이 사람', 'i saram', 'this person', '👤'],
            ['그 사람', 'geu saram', 'that person', '🧑'],
            ['이거', 'igeo', 'this one', '👇'],
            ['그거', 'geugeo', 'that one', '👉'],
            ['저거', 'jeogeo', 'that one over there', '👈'],
            ['누구', 'nugu', 'who', '❓'],
            ['모두', 'modu', 'everyone / all', '👥'],
            ['아무도', 'amudo', 'nobody', '🚫'],
            ['자기', 'jagi', 'oneself', '🪞'],
            ['서로', 'seoro', 'each other', '🔁']
          ]) }
      ] },

    /* ================= 2. THE NAVIGATORS ================= */
    { id: 'nav', title: 'The Navigators', sub: 'Location & quantity', emoji: '🧭', icon: 'ess-nav',
      blurb: 'Where things are and how many there are — the two questions travelling never stops asking.',
      sections: [

        { id: 'pp1', title: 'Where exactly', kind: 'Position words', emoji: '📐', icon: 'ess-position',
          note: 'Korean puts these AFTER the place: 학교 앞 = school front = in front of the school.',
          words: W([
            ['안', 'an', 'in / inside', '📦'],
            ['밖', 'bak', 'outside', '🌳'],
            ['위', 'wi', 'on / above', '⬆️'],
            ['아래', 'arae', 'under / below', '⬇️'],
            ['밑', 'mit', 'underneath', '🔽'],
            ['앞', 'ap', 'in front of', '➡️'],
            ['뒤', 'dwi', 'behind', '⬅️'],
            ['옆', 'yeop', 'next to', '↔️'],
            ['사이', 'sai', 'between', '🔀'],
            ['근처', 'geuncheo', 'near', '📍'],
            ['여기', 'yeogi', 'here', '📌'],
            ['거기', 'geogi', 'there', '📍'],
            ['저기', 'jeogi', 'over there', '🔭'],
            ['에', 'e', 'to / at (a place)', '🎯', '학교에 가요 = I go to school.'],
            ['에서', 'eseo', 'at / from (where it happens)', '🏠', '집에서 먹어요 = I eat at home.'],
            ['까지', 'kkaji', 'as far as / until', '🏁'],
            ['부터', 'buteo', 'from (a starting point)', '🚦']
          ]) },

        { id: 'num1', title: 'Counting numbers (하나, 둘, 셋)', kind: 'Numbers', emoji: '🔢', icon: 'ess-numbers1',
          note: 'The Korean set. Used for ages, hours on the clock, and counting things: 사과 세 개 = three apples.',
          words: W([
            ['하나', 'hana', 'one', '1️⃣'],
            ['둘', 'dul', 'two', '2️⃣'],
            ['셋', 'set', 'three', '3️⃣'],
            ['넷', 'net', 'four', '4️⃣'],
            ['다섯', 'daseot', 'five', '5️⃣'],
            ['여섯', 'yeoseot', 'six', '6️⃣'],
            ['일곱', 'ilgop', 'seven', '7️⃣'],
            ['여덟', 'yeodeol', 'eight', '8️⃣'],
            ['아홉', 'ahop', 'nine', '9️⃣'],
            ['열', 'yeol', 'ten', '🔟'],
            ['스물', 'seumul', 'twenty', '2️⃣0️⃣'],
            ['개', 'gae', 'counter for things', '📦', '두 개 주세요 = two of them, please.'],
            ['명', 'myeong', 'counter for people', '🧍'],
            ['마리', 'mari', 'counter for animals', '🐕'],
            ['살', 'sal', 'counter for age', '🎂'],
            ['시', 'si', 'o’clock', '🕐'],
            ['번', 'beon', 'counter for times / turns', '🔁']
          ]) },

        { id: 'num2', title: 'Money and time numbers (일, 이, 삼)', kind: 'Numbers', emoji: '💰', icon: 'ess-numbers2',
          note: 'The Sino-Korean set. Used for money, minutes, dates, phone numbers and floors.',
          words: W([
            ['일', 'il', 'one', '1️⃣'],
            ['이', 'i', 'two', '2️⃣'],
            ['삼', 'sam', 'three', '3️⃣'],
            ['사', 'sa', 'four', '4️⃣'],
            ['오', 'o', 'five', '5️⃣'],
            ['육', 'yuk', 'six', '6️⃣'],
            ['칠', 'chil', 'seven', '7️⃣'],
            ['팔', 'pal', 'eight', '8️⃣'],
            ['구', 'gu', 'nine', '9️⃣'],
            ['십', 'sip', 'ten', '🔟'],
            ['백', 'baek', 'hundred', '💯'],
            ['천', 'cheon', 'thousand', '🔢'],
            ['만', 'man', 'ten thousand', '💵', 'Korean jumps in ten-thousands: 만 원 = 10,000 won.'],
            ['원', 'won', 'won (money)', '🇰🇷'],
            ['분', 'bun', 'minute', '⏱️'],
            ['층', 'cheung', 'floor (of a building)', '🛗'],
            ['얼마예요?', 'eolmayeyo?', 'how much is it?', '💰']
          ]) }
      ] },

    /* ================= 3. THE MODIFIERS ================= */
    { id: 'mod', title: 'The Modifiers', sub: 'Detail & description', emoji: '🎨', icon: 'ess-mod',
      blurb: 'How something is, and how something is done. This is where a sentence stops being flat.',
      sections: [

        { id: 'adj1', title: 'Opposites', kind: 'Adjectives', emoji: '↔️', icon: 'ess-opposites',
          note: 'Learn them in pairs — it is half the work and twice the memory. Remember: these are already verbs, so 커요 means “is big”.',
          words: W([
            ['커요', 'keoyo', 'be big', '🐘'],
            ['작아요', 'jagayo', 'be small', '🐜'],
            ['많아요', 'manayo', 'be a lot', '➕'],
            ['적어요', 'jeogeoyo', 'be a little', '➖'],
            ['뜨거워요', 'tteugeowoyo', 'be hot', '♨️'],
            ['차가워요', 'chagawoyo', 'be cold', '🧊'],
            ['좋아요', 'joayo', 'be good', '👍'],
            ['나빠요', 'nappayo', 'be bad', '👎'],
            ['비싸요', 'bissayo', 'be expensive', '💸'],
            ['싸요', 'ssayo', 'be cheap', '🪙'],
            ['가까워요', 'gakkawoyo', 'be near', '📍'],
            ['멀어요', 'meoreoyo', 'be far', '🛣️'],
            ['빨라요', 'ppallayo', 'be fast', '💨'],
            ['느려요', 'neuryeoyo', 'be slow', '🐢'],
            ['쉬워요', 'swiwoyo', 'be easy', '😌'],
            ['어려워요', 'eoryeowoyo', 'be difficult', '😵'],
            ['무거워요', 'mugeowoyo', 'be heavy', '🪨', 'Its opposite, 가벼워요 (be light), is worth learning with it.']
          ]) },

        { id: 'adj2', title: 'Describing anything', kind: 'Adjectives', emoji: '✨', icon: 'ess-describe',
          note: 'The words you reach for when someone asks 어때요? — how is it?',
          words: W([
            ['맛있어요', 'masisseoyo', 'be delicious', '😋'],
            ['매워요', 'maewoyo', 'be spicy', '🌶️'],
            ['예뻐요', 'yeppeoyo', 'be pretty', '🌸'],
            ['재미있어요', 'jaemiisseoyo', 'be fun', '😄'],
            ['아파요', 'apayo', 'be sore / hurt', '🤕'],
            ['바빠요', 'bappayo', 'be busy', '🏃'],
            ['피곤해요', 'pigonhaeyo', 'be tired', '😪'],
            ['배고파요', 'baegopayo', 'be hungry', '🍽️'],
            ['새로워요', 'saerowoyo', 'be new', '🆕'],
            ['오래됐어요', 'oraedwaesseoyo', 'be old (a thing)', '🕰️'],
            ['깨끗해요', 'kkaekkeuthaeyo', 'be clean', '🫧'],
            ['더러워요', 'deoreowoyo', 'be dirty', '🧽'],
            ['조용해요', 'joyonghaeyo', 'be quiet', '🤫'],
            ['시끄러워요', 'sikkeureowoyo', 'be noisy', '📢'],
            ['위험해요', 'wiheomhaeyo', 'be dangerous', '⚠️'],
            ['안전해요', 'anjeonhaeyo', 'be safe', '🛡️'],
            ['친절해요', 'chinjeolhaeyo', 'be kind', '😇']
          ]) },

        { id: 'adv1', title: 'When', kind: 'Adverbs', emoji: '🕐', icon: 'ess-when',
          note: 'Time words go near the start of the sentence, before the verb.',
          words: W([
            ['지금', 'jigeum', 'now', '⏱️'],
            ['나중에', 'najunge', 'later', '🕘'],
            ['오늘', 'oneul', 'today', '📍'],
            ['내일', 'naeil', 'tomorrow', '➡️'],
            ['어제', 'eoje', 'yesterday', '⬅️'],
            ['아침', 'achim', 'morning', '🌅'],
            ['점심', 'jeomsim', 'midday / lunchtime', '🕛'],
            ['저녁', 'jeonyeok', 'evening', '🌆'],
            ['밤', 'bam', 'night', '🌙'],
            ['먼저', 'meonjeo', 'first', '1️⃣'],
            ['다음에', 'daeume', 'next time', '📆'],
            ['아직', 'ajik', 'not yet / still', '⏳'],
            ['벌써', 'beolsseo', 'already', '⚡'],
            ['곧', 'got', 'soon', '🔜'],
            ['오래', 'orae', 'for a long time', '🕰️'],
            ['잠깐', 'jamkkan', 'for a moment', '⏸️'],
            ['언제', 'eonje', 'when', '❓']
          ]) },

        { id: 'adv2', title: 'How and how often', kind: 'Adverbs', emoji: '🔁', icon: 'ess-howoften',
          note: 'Drop these straight in front of the verb: 천천히 말해 주세요.',
          words: W([
            ['빨리', 'ppalli', 'quickly', '💨'],
            ['천천히', 'cheoncheonhi', 'slowly', '🐢'],
            ['잘', 'jal', 'well', '👍'],
            ['많이', 'mani', 'a lot', '➕'],
            ['조금', 'jogeum', 'a little', '🤏'],
            ['너무', 'neomu', 'too (much)', '🔥'],
            ['아주', 'aju', 'very', '❗'],
            ['진짜', 'jinjja', 'really', '😮'],
            ['같이', 'gachi', 'together', '🤝'],
            ['혼자', 'honja', 'alone', '🧍'],
            ['항상', 'hangsang', 'always', '♾️'],
            ['보통', 'botong', 'usually', '📊'],
            ['가끔', 'gakkeum', 'sometimes', '🌗'],
            ['거의', 'geoui', 'almost / hardly', '📐'],
            ['전혀', 'jeonhyeo', 'not at all', '🚫'],
            ['다시', 'dasi', 'again', '🔁'],
            ['또', 'tto', 'again / also', '➕']
          ]) }
      ] },

    /* ================= 4. THE GLUE ================= */
    { id: 'glue', title: 'The Glue', sub: 'Structure & flow', emoji: '🔗', icon: 'ess-glue',
      blurb: 'What turns one-word answers into conversation — and what makes you sound like a person rather than a phrasebook.',
      sections: [

        { id: 'con1', title: 'Joining words', kind: 'Conjunctions', emoji: '➕', icon: 'ess-joining',
          note: 'Most of these start the second sentence rather than sitting in the middle — very different from English.',
          words: W([
            ['그리고', 'geurigo', 'and', '➕'],
            ['하고', 'hago', 'and (between two nouns)', '🔗', '빵하고 우유 = bread and milk.'],
            ['그런데', 'geureonde', 'but / by the way', '↩️'],
            ['하지만', 'hajiman', 'however', '⚖️'],
            ['그래서', 'geuraeseo', 'so / therefore', '➡️'],
            ['왜냐하면', 'waenyahamyeon', 'because', '💡'],
            ['때문에', 'ttaemune', 'because of', '📌'],
            ['또는', 'ttoneun', 'or', '🔀'],
            ['아니면', 'animyeon', 'or else', '🔃'],
            ['그럼', 'geureom', 'in that case', '👉'],
            ['만약에', 'manyage', 'if', '❔'],
            ['그때', 'geuttae', 'at that time', '⏳'],
            ['그다음에', 'geudaeume', 'after that', '⏭️'],
            ['처음에는', 'cheoeumeneun', 'at first', '1️⃣'],
            ['마지막에', 'majimage', 'in the end', '🏁'],
            ['예를 들면', 'yereul deulmyeon', 'for example', '📝'],
            ['그러니까', 'geureonikka', 'I mean / that’s why', '🗣️']
          ]) },

        { id: 'int1', title: 'Please, thank you, sorry', kind: 'Essential phrases', emoji: '🙏', icon: 'ess-please',
          note: 'The eight phrases that will get a child through almost any encounter in Korea.',
          words: W([
            ['안녕하세요', 'annyeonghaseyo', 'hello', '🙇'],
            ['감사합니다', 'gamsahamnida', 'thank you', '🙏'],
            ['죄송합니다', 'joesonghamnida', "I'm sorry", '🙇'],
            ['실례합니다', 'sillyehamnida', 'excuse me', '✋'],
            ['저기요', 'jeogiyo', 'excuse me (to a stranger)', '📣'],
            ['네', 'ne', 'yes', '✅'],
            ['아니요', 'aniyo', 'no', '❌'],
            ['괜찮아요', 'gwaenchanayo', "it's okay", '👌'],
            ['도와주세요', 'dowajuseyo', 'please help me', '🆘'],
            ['천천히 말해 주세요', 'cheoncheonhi malhae juseyo', 'please speak slowly', '🐢'],
            ['다시 말해 주세요', 'dasi malhae juseyo', 'please say it again', '🔁'],
            ['한국말 잘 못해요', 'hangungmal jal mothaeyo', "I don't speak Korean well", '😅'],
            ['영어 할 수 있어요?', 'yeongeo hal su isseoyo?', 'do you speak English?', '🔤'],
            ['이게 뭐예요?', 'ige mwoyeyo?', 'what is this?', '❓'],
            ['어디예요?', 'eodiyeyo?', 'where is it?', '📍'],
            ['안녕히 계세요', 'annyeonghi gyeseyo', 'goodbye (as you leave)', '👋'],
            ['안녕히 가세요', 'annyeonghi gaseyo', 'goodbye (to someone leaving)', '🚶']
          ]) },

        { id: 'int2', title: 'Sounding like a real person', kind: 'Fillers & reactions', emoji: '😮', icon: 'ess-fillers',
          note: 'Nobody teaches these, and they are exactly what makes a child sound Korean rather than translated.',
          words: W([
            ['아', 'a', 'ah', '💭'],
            ['어…', 'eo…', 'um…', '😐'],
            ['음…', 'eum…', 'hmm…', '🤔'],
            ['그…', 'geu…', 'er… (buying time)', '⏳'],
            ['진짜?', 'jinjja?', 'really?', '😮'],
            ['정말요?', 'jeongmaryo?', 'really? (polite)', '😯'],
            ['대박', 'daebak', 'wow / amazing', '🤩'],
            ['헐', 'heol', 'no way', '😱'],
            ['맞아요', 'majayo', "that's right", '✔️'],
            ['그래요?', 'geuraeyo?', 'oh really?', '🙂'],
            ['그렇구나', 'geureokuna', 'ah, I see', '💡'],
            ['알겠어요', 'algesseoyo', 'got it', '👌'],
            ['글쎄요', 'geulsseyo', 'hmm, not sure', '🤷'],
            ['잠깐만요', 'jamkkanmanyo', 'just a moment', '✋'],
            ['화이팅', 'hwaiting', 'you can do it!', '📣'],
            ['축하해요', 'chukhahaeyo', 'congratulations', '🎉'],
            ['수고하셨어요', 'sugohasyeosseoyo', 'well done / thanks for your work', '👏']
          ]) }
      ] }
  ];

  const sections = [];
  groups.forEach(g => g.sections.forEach(s => sections.push(Object.assign({ group: g.id, groupTitle: g.title }, s))));

  // Essentials deliberately repeats words the Path and Level 2 also teach — that is the point
  // of a survival list. Only the ones that appear nowhere else are added to the word bank.
  const all = [];
  sections.forEach(s => s.words.forEach(w => all.push(Object.assign({ ess: s.id, pack: s.kind }, w))));

  window.HQ_ESS = { groups, sections, words: all };
})();
