/* 한글 Quest — Level 2: 친구와 가족 (Friends & Family)
   Conversation content: word sets, grammar patterns and dialogues.
   Loads after data.js and merges its words into the shared word bank.

   Word rows are compact to keep this file readable:
     [ko, romanisation, english, emoji?, note?]
   Verbs and adjectives are stored in the 해요 form the children will actually say
   (먹어요, not 먹다), with the dictionary form in the note where it helps.        */
(function () {
  const W = rows => rows.map(r => ({ ko: r[0], rom: r[1], en: r[2], emoji: r[3] || '💬', note: r[4] || '' }));

  /* ---------- the cast ---------- */
  const cast = {
    minjun:   { name: '민준', rom: 'Minjun', en: 'your best friend, 10', talk: 'banmal' },
    haeun:    { name: '하은', rom: 'Haeun', en: 'your friend, 10 — draws comics', talk: 'banmal' },
    jiho:     { name: '지호', rom: 'Jiho', en: 'little cousin, 6', talk: 'banmal' },
    seoyeon:  { name: '서연', rom: 'Seoyeon', en: 'older cousin, 15', talk: 'banmal' },
    mum:      { name: '엄마', rom: 'Mum', en: 'Mum', talk: 'mixed' },
    dad:      { name: '아빠', rom: 'Dad', en: 'Dad', talk: 'mixed' },
    grandma:  { name: '할머니', rom: 'Grandma', en: 'Grandma', talk: 'jondaenmal' },
    grandpa:  { name: '할아버지', rom: 'Grandpa', en: 'Grandpa', talk: 'jondaenmal' },
    teacher:  { name: '박 선생님', rom: 'Ms Park', en: 'your class teacher', talk: 'jondaenmal' },
    aunt:     { name: '이모', rom: 'Imo', en: "Mum's sister", talk: 'jondaenmal' }
  };

  /* ---------- grammar patterns (the Sentence Lab) ---------- */
  const patterns = {
    p1a: {
      name: 'Saying what something is', ko: '이에요 / 예요',
      teach: 'To say “A is B”, put <b>이에요</b> or <b>예요</b> on the end. Use <b>이에요</b> after a consonant, <b>예요</b> after a vowel — whichever is easier to say.',
      examples: [['저는 학생이에요.', 'jeoneun haksaengieyo', 'I am a student.'],
                 ['제 이름은 민준이에요.', 'je ireumeun minjunieyo', 'My name is Minjun.'],
                 ['친구예요.', 'chinguyeyo', "It's my friend."]],
      build: { prompt: 'Build: “I am a student.”', tiles: ['저는', '학생', '이에요', '친구', '예요'], answer: ['저는', '학생', '이에요'] }
    },
    p1b: {
      name: 'The same thing to a friend', ko: '-이야 / -야',
      teach: 'Talking to a friend your own age? Drop the <b>요</b>. <b>이에요</b> becomes <b>이야</b>, <b>예요</b> becomes <b>야</b>. That’s <b>반말</b> — casual speech.',
      examples: [['나는 학생이야.', 'naneun haksaengiya', "I'm a student."],
                 ['내 이름은 하은이야.', 'nae ireumeun haeuniya', "My name's Haeun."],
                 ['내 친구야.', 'nae chinguya', "It's my friend."]],
      build: { prompt: 'Say “My name is Haeun” to a friend.', tiles: ['내', '이름은', '하은이야', '제', '하은이에요'], answer: ['내', '이름은', '하은이야'] }
    },
    p2a: {
      name: 'Have and have not', ko: '있어요 / 없어요',
      teach: '<b>있어요</b> = there is / I have. <b>없어요</b> = there isn’t / I don’t have. Two words that do an enormous amount of work.',
      examples: [['동생이 있어요.', 'dongsaengi isseoyo', 'I have a younger sibling.'],
                 ['형은 없어요.', 'hyeongeun eopseoyo', "I don't have an older brother."],
                 ['강아지 있어?', 'gangaji isseo?', 'Have you got a dog?']],
      build: { prompt: 'Build: “I have a younger sibling.”', tiles: ['동생이', '있어요', '없어요', '형이'], answer: ['동생이', '있어요'] }
    },
    p2b: {
      name: 'The topic marker', ko: '은 / 는',
      teach: 'Stick <b>은</b> or <b>는</b> on the thing you’re talking <i>about</i>: “as for me…”, “as for my brother…”. Use <b>은</b> after a consonant, <b>는</b> after a vowel.',
      examples: [['저는 뉴질랜드 사람이에요.', 'jeoneun nyujillaendeu saramieyo', 'I am from New Zealand.'],
                 ['우리 형은 열다섯 살이에요.', 'uri hyeongeun yeoldaseot sarieyo', 'My big brother is fifteen.'],
                 ['엄마는 선생님이에요.', 'eommaneun seonsaengnimieyo', 'Mum is a teacher.']],
      build: { prompt: 'Build: “Mum is a teacher.”', tiles: ['엄마는', '선생님이에요', '엄마가', '있어요'], answer: ['엄마는', '선생님이에요'] }
    }
  };

  /* ---------- units ---------- */
  const units = [

    /* ============================ UNIT 1 ============================ */
    { id: 1, ko: '안녕, 나야', title: 'Hello & me', emoji: '👋', img: 'u1-hello', stamp: 'u1-hello',
      blurb: 'Say hello, give your name and age, and meet someone new — politely and casually.',
      can: ['say hello to a friend and to a grown-up', 'give my name and age', 'say where I am from', 'ask someone the same things'],
      patterns: ['p1a', 'p1b'],
      sets: [
        { id: '1a', title: 'Hello and goodbye', words: W([
          ['안녕', 'annyeong', 'hi / bye (to a friend)', '👋'],
          ['여보세요', 'yeoboseyo', 'hello (on the phone)', '📞'],
          ['안녕히 가세요', 'annyeonghi gaseyo', 'goodbye (to someone leaving)', '👋'],
          ['안녕히 계세요', 'annyeonghi gyeseyo', 'goodbye (said as you leave)', '🚪'],
          ['반가워', 'bangawo', 'nice to meet you (friend)', '😄'],
          ['반갑습니다', 'bangapseumnida', 'nice to meet you (polite)', '🤝'],
          ['오랜만이야', 'oraenmaniya', 'long time no see', '😲'],
          ['잘 가', 'jal ga', 'bye, go well', '🚶'],
          ['고마워', 'gomawo', 'thanks (friend)', '🙏'],
          ['실례합니다', 'sillyehamnida', 'excuse me', '🙇'],
          ['미안해', 'mianhae', 'sorry (friend)', '😔'],
          ['죄송합니다', 'joesonghamnida', 'I’m sorry (polite)', '🙇'],
          ['괜찮아', 'gwaenchana', "it's okay (friend)", '👌'],
          ['잘 있어', 'jal isseo', 'bye, stay well', '👋'],
          ['응', 'eung', 'yeah (friend)', '✅'],
          ['천만에요', 'cheonmaneyo', "you're welcome", '🙂'],
          ['아니', 'ani', 'nope (friend)', '❌']
        ]) },
        { id: '1b', title: 'Me and you', words: W([
          ['저희', 'jeohui', 'we / our (polite)', '👥'],
          ['저', 'jeo', 'I / me (polite)', '🙇'],
          ['별명', 'byeolmyeong', 'nickname', '🏷️'],
          ['우리', 'uri', 'we / our', '👨‍👩‍👧'],
          ['이름', 'ireum', 'name', '🏷️'],
          ['나이', 'nai', 'age', '🎂'],
          ['살', 'sal', 'years old', '🎂', 'Used with the Korean numbers: 열 살 = ten years old.'],
          ['몇', 'myeot', 'how many / what (number)', '🔢'],
          ['짝', 'jjak', 'the person you sit next to', '🧑‍🤝‍🧑'],
          ['반 친구', 'ban chingu', 'classmate', '🧑‍🏫'],
          ['선배', 'seonbae', 'someone older at school', '🎓'],
          ['학생', 'haksaeng', 'student', '🎒'],
          ['초등학생', 'chodeunghaksaeng', 'primary school pupil', '🏫'],
          ['어린이', 'eorini', 'child', '🧒'],
          ['남자', 'namja', 'boy / man', '👦'],
          ['후배', 'hubae', 'someone younger at school', '🌱'],
          ['우리 반', 'uri ban', 'my class', '🧑‍🏫']
        ]) },
        { id: '1c', title: 'Where I am from', words: W([
          ['국기', 'gukgi', 'flag', '🚩'],
          ['고향', 'gohyang', 'hometown', '🏡'],
          ['한국 사람', 'hanguk saram', 'Korean person', '🇰🇷'],
          ['뉴질랜드', 'nyujillaendeu', 'New Zealand', '🇳🇿'],
          ['호주', 'hoju', 'Australia', '🇦🇺'],
          ['영국', 'yeongguk', 'the UK', '🇬🇧'],
          ['미국', 'miguk', 'the USA', '🇺🇸'],
          ['일본', 'ilbon', 'Japan', '🇯🇵'],
          ['중국', 'jungguk', 'China', '🇨🇳'],
          ['외국', 'oeguk', 'a foreign country', '✈️'],
          ['외국인', 'oegugin', 'foreigner', '🧳'],
          ['영어', 'yeongeo', 'English (language)', '🔤'],
          ['한국말', 'hangungmal', 'Korean (language)', '🗣️'],
          ['살아요', 'sarayo', 'live (somewhere)', '🏠', 'Dictionary form: 살다.'],
          ['이사해요', 'isahaeyo', 'move house', '📦'],
          ['도시', 'dosi', 'city', '🏙️'],
          ['시골', 'sigol', 'countryside', '🌾']
        ]) },
        { id: '1d', title: 'Meeting someone', words: W([
          ['만나요', 'mannayo', 'meet', '🤝', 'Dictionary form: 만나다.'],
          ['처음', 'cheoeum', 'the first time', '1️⃣'],
          ['말해요', 'malhaeyo', 'say / speak', '💬'],
          ['물어봐요', 'mureobwayo', 'ask', '❓'],
          ['대답해요', 'daedaphaeyo', 'answer', '🙋'],
          ['소개해요', 'sogaehaeyo', 'introduce', '👋'],
          ['알아요', 'arayo', 'know', '💡'],
          ['몰라요', 'mollayo', "don't know", '🤷'],
          ['천천히', 'cheoncheonhi', 'slowly', '🐢'],
          ['다시', 'dasi', 'again', '🔁'],
          ['조금', 'jogeum', 'a little', '🤏'],
          ['잘', 'jal', 'well', '👍'],
          ['못', 'mot', "can't", '🚫'],
          ['진짜', 'jinjja', 'really / for real', '😮'],
          ['정말', 'jeongmal', 'really (polite)', '😮'],
          ['맞아', 'maja', "that's right", '✔️'],
          ['대박', 'daebak', 'wow / amazing', '🤩']
        ]) },
        { id: '1e', title: 'Friend talk or grown-up talk', words: W([
          ['반말', 'banmal', 'casual speech (to friends)', '🧒'],
          ['높임말', 'nopimmal', 'polite speech (to grown-ups)', '👵'],
          ['어른', 'eoreun', 'grown-up', '🧑'],
          ['존댓말', 'jondaenmal', 'polite speech (another word for 높임말)', '👔'],
          ['말투', 'maltu', 'way of speaking / tone', '🗣️'],
          ['공손해요', 'gongsonhaeyo', 'be polite', '🎩'],
          ['버릇없어요', 'beoreudeopseoyo', 'be rude / have no manners', '😠'],
          ['동생', 'dongsaeng', 'younger brother or sister', '🧒'],
          ['선생님', 'seonsaengnim', 'teacher', '🧑‍🏫'],
          ['불러요', 'bulleoyo', 'call (someone something)', '📣'],
          ['인사해요', 'insahaeyo', 'greet / say hello', '🙇'],
          ['예의', 'yeui', 'manners', '🎩'],
          ['그치?', 'geuchi?', "right? / don't you think?", '🙃'],
          ['그래', 'geurae', 'okay / sure', '👌'],
          ['아니야', 'aniya', "it's not", '🙅'],
          ['글쎄', 'geulsse', 'hmm, not sure', '🤔'],
          ['처음 뵙겠습니다', 'cheoeum boepgesseumnida', 'how do you do (very polite)', '🤝']
        ]) }
      ],
      dialogues: [
        { id: 'd1a', title: 'Meeting 민준', talk: 'banmal', scene: 'playground', with: ['minjun'],
          intro: 'A boy on the playground kicks a ball over to you and grins.',
          turns: [
            { who: 'minjun', ko: '안녕! 나는 민준이야.', rom: 'annyeong! naneun minjuniya', en: "Hi! I'm Minjun.",
              q: { kind: 'reply', prompt: 'Say hi back and give your name. (He’s your age — 반말.)',
                options: [{ ko: '안녕! 나는 ○○이야.', rom: 'annyeong! naneun ○○iya', en: "Hi! I'm ○○.", ok: 1 },
                          { ko: '안녕하세요. 저는 ○○입니다.', rom: 'annyeonghaseyo. jeoneun ○○imnida', en: 'Hello. My name is ○○. (very formal)' },
                          { ko: '안녕히 계세요.', rom: 'annyeonghi gyeseyo', en: 'Goodbye.' }],
                tip: 'To someone your own age you drop the 요. 나는 … 이야 is the friend version of 저는 … 이에요.' } },
            { who: 'minjun', ko: '너 몇 살이야?', rom: 'neo myeot sariya?', en: 'How old are you?',
              q: { kind: 'reply', prompt: 'You’re ten. Tell him.',
                options: [{ ko: '열 살이야.', rom: 'yeol sariya', en: "I'm ten.", ok: 1 },
                          { ko: '열 시야.', rom: 'yeol siya', en: "It's ten o'clock." },
                          { ko: '열 개야.', rom: 'yeol gaeya', en: 'There are ten of them.' }],
                tip: '살 counts years of age. 시 counts hours, 개 counts things — easy to mix up!' } },
            { who: 'minjun', ko: '나도 열 살이야! 어디에서 왔어?', rom: 'nado yeol sariya! eodieseo wasseo?', en: "I'm ten too! Where are you from?",
              q: { kind: 'reply', prompt: 'Tell him you came from New Zealand.',
                options: [{ ko: '뉴질랜드에서 왔어.', rom: 'nyujillaendeueseo wasseo', en: 'I came from New Zealand.', ok: 1 },
                          { ko: '뉴질랜드에 갔어.', rom: 'nyujillaendeue gasseo', en: 'I went to New Zealand.' },
                          { ko: '뉴질랜드가 좋아.', rom: 'nyujillaendeuga joa', en: 'I like New Zealand.' }],
                tip: '에서 왔어 = came *from*. 에 갔어 = went *to*.' } },
            { who: 'minjun', ko: '우와, 진짜? 한국말 잘하네!', rom: 'uwa, jinjja? hangungmal jalhane!', en: 'Whoa, really? Your Korean is good!',
              q: { kind: 'listen', ko: '한국말 잘하네!', rom: 'hangungmal jalhane!', prompt: 'What did 민준 just say?',
                options: [{ en: 'Your Korean is good!', ok: 1 }, { en: 'Do you speak Korean?' }, { en: "I can't speak Korean." }],
                tip: 'Koreans say this to anyone who tries. Accept it with 아니야, 조금밖에 못 해 — “no, only a little”.' } },
            { who: 'minjun', ko: '우리 친구 하자!', rom: 'uri chingu haja!', en: "Let's be friends!",
              q: { kind: 'say', ko: '응, 좋아! 반가워!', rom: 'eung, joa! bangawo!', en: 'Yeah, great! Nice to meet you!',
                note: 'You just made a Korean friend. Say it out loud like you mean it.' } }
          ] },
        { id: 'd1b', title: 'Hello, 할머니', talk: 'jondaenmal', scene: 'home-hallway', with: ['grandma'],
          intro: 'Your friend’s grandmother opens the door. Time for your best manners.',
          turns: [
            { who: 'grandma', ko: '어서 와요! 누구세요?', rom: 'eoseo wayo! nuguseyo?', en: 'Come in! Who is this?',
              q: { kind: 'reply', prompt: 'Greet her politely and give your name.',
                options: [{ ko: '안녕하세요. 저는 ○○이에요.', rom: 'annyeonghaseyo. jeoneun ○○ieyo', en: "Hello. I'm ○○.", ok: 1 },
                          { ko: '안녕! 나는 ○○이야.', rom: 'annyeong! naneun ○○iya', en: "Hi! I'm ○○. (to a friend)" },
                          { ko: '누구세요?', rom: 'nuguseyo?', en: 'Who are you?' }],
                tip: 'Same sentence as with 민준 — but to a grandparent every ending gets its 요 back.' } },
            { who: 'grandma', ko: '아이고, 반가워요. 몇 살이에요?', rom: 'aigo, bangawoyo. myeot sarieyo?', en: 'Oh, lovely to meet you. How old are you?',
              q: { kind: 'reply', prompt: 'Tell her politely.',
                options: [{ ko: '열 살이에요.', rom: 'yeol sarieyo', en: "I'm ten.", ok: 1 },
                          { ko: '열 살이야.', rom: 'yeol sariya', en: "I'm ten. (to a friend)" },
                          { ko: '몇 살이에요?', rom: 'myeot sarieyo?', en: 'How old are you?' }],
                tip: '아이고 is the little sound Korean grandparents make about absolutely everything.' } },
            { who: 'grandma', ko: '어느 나라에서 왔어요?', rom: 'eoneu naraeseo wasseoyo?', en: 'Which country are you from?',
              q: { kind: 'reply', prompt: 'Answer politely.',
                options: [{ ko: '뉴질랜드에서 왔어요.', rom: 'nyujillaendeueseo wasseoyo', en: 'I came from New Zealand.', ok: 1 },
                          { ko: '뉴질랜드에서 왔어.', rom: 'nyujillaendeueseo wasseo', en: 'I came from New Zealand. (casual)' },
                          { ko: '한국 사람이에요.', rom: 'hanguk saramieyo', en: 'I am Korean.' }] } },
            { who: 'grandma', ko: '많이 먹어요. 과일 먹을래요?', rom: 'mani meogeoyo. gwail meogeullaeyo?', en: 'Eat lots. Would you like some fruit?',
              q: { kind: 'listen', ko: '과일 먹을래요?', rom: 'gwail meogeullaeyo?', prompt: 'What is she offering you?',
                options: [{ en: 'Some fruit', ok: 1 }, { en: 'A drink' }, { en: 'A chair' }],
                tip: 'Korean grandmothers feed people. Saying yes is the polite answer.' } },
            { q: { kind: 'say', ko: '네, 감사합니다!', rom: 'ne, gamsahamnida!', en: 'Yes, thank you!',
                note: 'Take it with two hands — that’s the polite way to receive anything from someone older.' } }
          ] }
      ] },

    /* ============================ UNIT 2 ============================ */
    { id: 2, ko: '우리 가족', title: 'My family', emoji: '👨‍👩‍👧‍👦', img: 'u2-family', stamp: 'u2-family',
      blurb: 'Talk about who is in your family, how old they are, and what they do.',
      can: ['name everyone in my family', 'say who I have and haven’t got', 'say how old they are', 'ask about someone else’s family'],
      patterns: ['p2a', 'p2b'],
      sets: [
        { id: '2a', title: 'The family', words: W([
          ['가족', 'gajok', 'family', '👨‍👩‍👧'],
          ['식구', 'sikgu', 'member of the household', '🏠'],
          ['외동', 'oedong', 'only child', '1️⃣'],
          ['부부', 'bubu', 'a married couple', '💑'],
          ['손자', 'sonja', 'grandson', '👦'],
          ['부모님', 'bumonim', 'parents', '👫'],
          ['할머니', 'halmeoni', 'grandma', '👵'],
          ['할아버지', 'harabeoji', 'grandpa', '👴'],
          ['남동생', 'namdongsaeng', 'younger brother', '👦'],
          ['여동생', 'yeodongsaeng', 'younger sister', '👧'],
          ['아들', 'adeul', 'son', '👦'],
          ['딸', 'ttal', 'daughter', '👧'],
          ['형제', 'hyeongje', 'brothers / siblings', '👬'],
          ['자매', 'jamae', 'sisters', '👭'],
          ['막내', 'mangnae', 'the youngest one', '🐣'],
          ['첫째', 'cheotjjae', 'the eldest one', '1️⃣'],
          ['손녀', 'sonnyeo', 'granddaughter', '👧']
        ]) },
        { id: '2b', title: 'Aunties, uncles and cousins', words: W([
          ['외할머니', 'oehalmeoni', "mum's mother", '👵'],
          ['고모', 'gomo', "dad's sister", '👩'],
          ['삼촌', 'samchon', 'uncle', '👨'],
          ['사촌', 'sachon', 'cousin', '🧒'],
          ['조카', 'joka', 'niece / nephew', '👶'],
          ['아기', 'agi', 'baby', '👶'],
          ['쌍둥이', 'ssangdungi', 'twins', '👯'],
          ['친척', 'chincheok', 'relatives', '👨‍👩‍👧‍👦'],
          ['친해요', 'chinhaeyo', 'be close (with someone)', '💞'],
          ['닮았어요', 'darmasseoyo', 'look alike', '👯'],
          ['같이 살아요', 'gachi sarayo', 'live together', '🏠'],
          ['따로', 'ttaro', 'separately', '↔️'],
          ['가까워요', 'gakkawoyo', 'be near', '📍'],
          ['멀어요', 'meoreoyo', 'be far', '🛣️'],
          ['자주', 'jaju', 'often', '🔁'],
          ['가끔', 'gakkeum', 'sometimes', '🌗'],
          ['매일', 'maeil', 'every day', '📅']
        ]) },
        { id: '2c', title: 'How many? (and have / have not)', words: W([
          ['있어요', 'isseoyo', 'there is / I have', '✅'],
          ['없어요', 'eopseoyo', "there isn't / I don't have", '❌'],
          ['명', 'myeong', 'counter for people', '🧍'],
          ['마리', 'mari', 'counter for animals', '🐕'],
          ['몇 명', 'myeot myeong', 'how many people', '🔢'],
          ['혼자', 'honja', 'alone / on my own', '🧍'],
          ['한', 'han', 'one (before a counter)', '1️⃣'],
          ['두', 'du', 'two (before a counter)', '2️⃣'],
          ['세', 'se', 'three (before a counter)', '3️⃣'],
          ['적어요', 'jeogeoyo', 'there are few', '➖'],
          ['다섯', 'daseot', 'five', '5️⃣'],
          ['여섯', 'yeoseot', 'six', '6️⃣'],
          ['일곱', 'ilgop', 'seven', '7️⃣'],
          ['여덟', 'yeodeol', 'eight', '8️⃣'],
          ['아홉', 'ahop', 'nine', '9️⃣'],
          ['열', 'yeol', 'ten', '🔟'],
          ['많아요', 'manayo', 'there are many', '➕']
        ]) },
        { id: '2d', title: 'Our house', words: W([
          ['우리 집', 'uri jip', 'our house', '🏠'],
          ['아파트', 'apateu', 'flat / apartment', '🏢'],
          ['층', 'cheung', 'floor (of a building)', '🛗'],
          ['방', 'bang', 'room', '🚪'],
          ['내 방', 'nae bang', 'my room', '🛏️'],
          ['거실', 'geosil', 'living room', '🛋️'],
          ['부엌', 'bueok', 'kitchen', '🍳'],
          ['옷장', 'otjang', 'wardrobe', '👚'],
          ['문', 'mun', 'door', '🚪'],
          ['창문', 'changmun', 'window', '🪟'],
          ['침대', 'chimdae', 'bed', '🛏️'],
          ['소파', 'sopa', 'sofa', '🛋️'],
          ['식탁', 'siktak', 'dining table', '🍽️'],
          ['냉장고', 'naengjanggo', 'fridge', '🧊'],
          ['텔레비전', 'tellebijeon', 'television', '📺'],
          ['사진', 'sajin', 'photo', '📷'],
          ['마당', 'madang', 'yard / garden', '🌳']
        ]) },
        { id: '2e', title: 'What they do', words: W([
          ['일해요', 'ilhaeyo', 'work', '💼'],
          ['사무실', 'samusil', 'office room', '🏢'],
          ['소방관', 'sobanggwan', 'firefighter', '🚒'],
          ['시장', 'sijang', 'market', '🧺'],
          ['회사원', 'hoesawon', 'office worker', '💼'],
          ['간호사', 'ganhosa', 'nurse', '💉'],
          ['경찰', 'gyeongchal', 'police officer', '👮'],
          ['요리사', 'yorisa', 'chef', '👨‍🍳'],
          ['운전해요', 'unjeonhaeyo', 'drive', '🚗'],
          ['요리해요', 'yorihaeyo', 'cook', '🍳'],
          ['청소해요', 'cheongsohaeyo', 'clean', '🧹'],
          ['쉬어요', 'swieoyo', 'rest', '😌'],
          ['바빠요', 'bappayo', 'be busy', '🏃'],
          ['재미있어요', 'jaemiisseoyo', 'be fun', '😄'],
          ['착해요', 'chakhaeyo', 'be kind', '😇'],
          ['웃겨요', 'utgyeoyo', 'be funny', '🤣'],
          ['무서워요', 'museowoyo', 'be scary', '😨']
        ]) }
      ],
      dialogues: [
        { id: 'd2a', title: 'The family photo', talk: 'banmal', scene: 'home-bedroom', with: ['haeun'],
          intro: '하은 spots a photo on your desk and picks it up.',
          turns: [
            { who: 'haeun', ko: '어? 이거 너희 가족이야?', rom: 'eo? igeo neohui gajogiya?', en: 'Oh? Is this your family?',
              q: { kind: 'reply', prompt: 'Yes, it is.',
                options: [{ ko: '응, 우리 가족이야.', rom: 'eung, uri gajogiya', en: "Yeah, that's my family.", ok: 1 },
                          { ko: '아니, 내 친구야.', rom: 'ani, nae chinguya', en: "No, that's my friend." },
                          { ko: '응, 우리 집이야.', rom: 'eung, uri jibiya', en: "Yeah, that's my house." }],
                tip: 'Koreans say 우리 (our) where English says “my”: 우리 가족, 우리 집, 우리 엄마.' } },
            { who: 'haeun', ko: '가족이 몇 명이야?', rom: 'gajogi myeot myeongiya?', en: 'How many people are in your family?',
              q: { kind: 'reply', prompt: 'There are four of you.',
                options: [{ ko: '네 명이야.', rom: 'ne myeongiya', en: 'There are four.', ok: 1 },
                          { ko: '네 개야.', rom: 'ne gaeya', en: 'There are four things.' },
                          { ko: '네 살이야.', rom: 'ne sariya', en: 'I am four years old.' }],
                tip: 'People are counted with 명. Never 개 — that’s for objects!' } },
            { who: 'haeun', ko: '형제 있어?', rom: 'hyeongje isseo?', en: 'Have you got any brothers or sisters?',
              q: { kind: 'reply', prompt: 'You have a younger sister, but no older brother.',
                options: [{ ko: '여동생 있어. 형은 없어.', rom: 'yeodongsaeng isseo. hyeongeun eopseo', en: "I've got a little sister. No older brother.", ok: 1 },
                          { ko: '여동생 없어. 형은 있어.', rom: 'yeodongsaeng eopseo. hyeongeun isseo', en: "No little sister. I've got an older brother." },
                          { ko: '여동생이 좋아.', rom: 'yeodongsaengi joa', en: 'I like little sisters.' }],
                tip: '있어 / 없어 — the two most useful words in this whole unit.' } },
            { who: 'haeun', ko: '동생 몇 살이야?', rom: 'dongsaeng myeot sariya?', en: 'How old is your sister?',
              q: { kind: 'listen', ko: '동생 몇 살이야?', rom: 'dongsaeng myeot sariya?', prompt: 'What is 하은 asking?',
                options: [{ en: "How old is your younger sibling?", ok: 1 }, { en: 'Do you have a younger sibling?' }, { en: 'What is your sister called?' }] } },
            { q: { kind: 'say', ko: '일곱 살이야. 진짜 웃겨!', rom: 'ilgop sariya. jinjja utgyeo!', en: "She's seven. She's so funny!",
                note: 'Swap in your own sibling’s age — and say what they’re really like.' } }
          ] },
        { id: 'd2b', title: 'Telling 선생님 about your family', talk: 'jondaenmal', scene: 'classroom', with: ['teacher'],
          intro: '박 선생님 asks you to tell the class about your family.',
          turns: [
            { who: 'teacher', ko: '가족을 소개해 주세요.', rom: 'gajogeul sogaehae juseyo', en: 'Please introduce your family.',
              q: { kind: 'reply', prompt: 'Start: “There are four people in my family.”',
                options: [{ ko: '우리 가족은 네 명이에요.', rom: 'uri gajogeun ne myeongieyo', en: 'There are four people in my family.', ok: 1 },
                          { ko: '우리 가족은 네 살이에요.', rom: 'uri gajogeun ne sarieyo', en: 'My family is four years old.' },
                          { ko: '우리 집은 네 명이에요.', rom: 'uri jibeun ne myeongieyo', en: 'My house is four people.' }],
                tip: '은/는 marks what you are talking about: 우리 가족은 … = “as for my family …”.' } },
            { who: 'teacher', ko: '어머니는 무슨 일을 하세요?', rom: 'eomeonineun museun ireul haseyo?', en: 'What does your mother do?',
              q: { kind: 'reply', prompt: 'Mum is a teacher.',
                options: [{ ko: '엄마는 선생님이에요.', rom: 'eommaneun seonsaengnimieyo', en: 'Mum is a teacher.', ok: 1 },
                          { ko: '엄마는 선생님이야.', rom: 'eommaneun seonsaengnimiya', en: 'Mum is a teacher. (casual)' },
                          { ko: '엄마는 학교예요.', rom: 'eommaneun hakgyoyeyo', en: 'Mum is a school.' }] } },
            { who: 'teacher', ko: '아버지는요?', rom: 'abeojineunyo?', en: 'And your father?',
              q: { kind: 'reply', prompt: 'Dad works at a hospital.',
                options: [{ ko: '아빠는 병원에서 일해요.', rom: 'appaneun byeongwoneseo ilhaeyo', en: 'Dad works at a hospital.', ok: 1 },
                          { ko: '아빠는 병원이에요.', rom: 'appaneun byeongwonieyo', en: 'Dad is a hospital.' },
                          { ko: '아빠는 병원에 있어요.', rom: 'appaneun byeongwone isseoyo', en: 'Dad is at the hospital (right now).' }],
                tip: '…에서 일해요 = works *at* somewhere. Handy for every job.' } },
            { who: 'teacher', ko: '아주 잘했어요!', rom: 'aju jalhaesseoyo!', en: 'Very well done!',
              q: { kind: 'listen', ko: '아주 잘했어요!', rom: 'aju jalhaesseoyo!', prompt: 'What did your teacher say?',
                options: [{ en: 'Very well done!', ok: 1 }, { en: 'Please say it again.' }, { en: "That's not quite right." }] } },
            { q: { kind: 'say', ko: '감사합니다!', rom: 'gamsahamnida!', en: 'Thank you!',
                note: 'A small bow of the head goes with it.' } }
          ] }
      ] }
  ];

  /* words carry their unit and set so the word bank, games and review can find them */
  const words = [];
  units.forEach(u => u.sets.forEach(s => s.words.forEach(w => {
    words.push(Object.assign({ lvl: 2, unit: u.id, set: s.id, stage: 100 + u.id, pack: s.title }, w));
  })));

  window.HQ_L2 = { units, patterns, cast, words };
})();
