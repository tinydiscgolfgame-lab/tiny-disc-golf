from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'data-tab="reward">Reward Roll</button>' in s:
    print('Reward Roll already exists in index.html')
else:
    tab = '<button class="tab" data-tab="courses">Courses</button>'
    if tab not in s:
        raise SystemExit('Courses tab not found')
    s = s.replace(tab, tab + '<button class="tab" data-tab="reward">Reward Roll</button>', 1)
    s = s.replace('.tabs{display:grid;grid-template-columns:repeat(10,1fr)', '.tabs{display:grid;grid-template-columns:repeat(11,1fr)', 1)

    section = '''<section id="reward" class="panel"><div class="tool"><h3>Reward Rolls</h3><p class="note">In Tiny Disc Golf, when a Player performs a spectacular feat like throwing in an Ace or winning a League or Tournament, then you have the chance to earn a random Reward from the Reward Roll Chart below. As with Success Rolls, a lower roll being better and wins the Player the best benefit!</p><button class="primary" id="rollReward">ROLL REWARD 1–100</button><div class="big" id="rewardNumber">—</div><div class="result" id="rewardResult">—</div><div id="rewardTable"></div><div class="modifier-section"><h3>Special Abilities (SA) Discs</h3><p class="note">If you were rewarded a SA Disc from your Reward Roll, choose the mold of disc you want and then roll once again to determine the type of Special Ability that disc has. So, if your putting is atrocious, you might want a SA Putter or if your Driving is subpar, you might choose a Driver and then roll to see how that disc has been changed to help your game!</p><button class="primary" id="rollSaDisc">ROLL SA DISC 1–100</button><div class="big" id="saNumber">—</div><div class="result" id="saResult">—</div><div id="saTable"></div></div></div></section>'''
    marker = '<section id="direction" class="panel">'
    if marker not in s:
        raise SystemExit('Direction panel not found')
    s = s.replace(marker, section + marker, 1)

    js = r'''const rewardRolls=[[1,1,'+2 to all Player Stats, + SA Disc & +15% Accessory'],[2,2,'+2 to all Player Stats'],[3,3,'SA Disc & +15% to Success Rolls Accessory of choice'],[4,5,'SA Disc'],[6,10,'Training Session! +5 to be spread among Player Stats'],[11,15,'Training Session! +5 to be spread among Player Stats'],[16,20,'Training Session! +1 to each Player Stats'],[21,25,'Training Session! +1 to Player Stat of choice'],[26,30,'Cart! +20% to all Success Rolls due to lack of fatigue'],[31,35,'Grip Enhancer! +15% to Success Rolls'],[36,40,'+1 Slot in Bag'],[41,45,'+10% to Success Rolls Accessory of choice'],[46,50,'+5% to Success Rolls Accessory of choice'],[51,55,'Umbrella & DG Gloves! Disregard rain related modifiers'],[56,60,'Lucky Charm! Roll 2 dice at beginning of round…If results are below 10 then the Player has Double Luck Points for that round'],[61,65,'Rangefinder! +15% to all tee shots'],[66,70,'Disc Golf Shoes! +10% to all Success Rolls'],[71,75,'Rating Increases by triple for this round'],[76,80,'Cooler Full of Beverages! Roll 2 dice at beginning of round…if over 50, then the Player has no Luck Points for that round, but if under then Luck Points are double that round'],[81,85,'Almost There! Just not enough to be noticed'],[86,90,'False Plateau! Thought Player made gains, but you didn’t'],[91,95,'In your own head! Great victory but Player gains nothing'],[96,96,'Hard high five from your homie causes a hand injury! -2 to all Player Stats for 5 rounds'],[97,97,'Left on Course! Lost your favorite Accessory for 5 rounds'],[98,98,'Left on Course! Lost your favorite Disc for 5 rounds'],[99,99,'Stolen Bag! You can’t use your usual Bag, Discs and Accessories for 5 rounds and your backup bag only has 6 slots'],[100,100,'Freak injury while celebrating! -2 to all Player Stats for 10 rounds & the Player’s favorite SA Disc is lost forever']];
const saDiscRolls=[[1,10,'All Modifiers are nullified'],[11,20,'All Course Modifiers are nullified'],[21,30,'All Hole Modifiers are nullified'],[31,40,'All Course Modifiers are nullified'],[41,50,'Power Disc! The Power of this disc does not factor into calculating Success Rolls & +20 feet/2” to all throws'],[51,60,'Control Disc! +25% to all Success Rolls'],[61,70,'Putting Disc! +35% to all Putts'],[71,80,'Lucky Disc! The disc itself has its own Luck equal to the Players Luck Stat that can be spent during a round'],[81,90,'+20% to all Success Rolls'],[91,100,'+10% to all Success Rolls']];
function findReward(n){return rewardRolls.find(r=>n>=r[0]&&n<=r[1])}
function findSaReward(n){return saDiscRolls.find(r=>n>=r[0]&&n<=r[1])}
function rewardTableHtml(rows){return '<div class="distance-table-wrap"><table class="distance-table"><thead><tr><th>Roll</th><th>Reward</th></tr></thead><tbody>'+rows.map(r=>'<tr><td>'+r[0]+(r[0]===r[1]?'':'–'+r[1])+'</td><td style="text-align:left">'+escapeDistanceHtml(r[2])+'</td></tr>').join('')+'</tbody></table></div>'}
function renderRewardTables(){const rt=$('#rewardTable'),st=$('#saTable');if(rt)rt.innerHTML=rewardTableHtml(rewardRolls);if(st)st.innerHTML=rewardTableHtml(saDiscRolls)}
function initRewardRoll(){renderRewardTables();$('#rollReward')?.addEventListener('click',()=>{const n=Math.floor(Math.random()*100)+1;const r=findReward(n);$('#rewardNumber').textContent=n;$('#rewardResult').textContent=r?r[2]:'—'});$('#rollSaDisc')?.addEventListener('click',()=>{const n=Math.floor(Math.random()*100)+1;const r=findSaReward(n);$('#saNumber').textContent=n;$('#saResult').textContent=r?r[2]:'—'})}
'''
    if 'const rewardRolls=[' in s:
        raise SystemExit('Reward Roll JS unexpectedly already exists')
    s = s.replace('const clickableModifiers=', js + 'const clickableModifiers=', 1)

    init_marker = 'loadPlayers();renderPlayers();renderRoundPlayers();renderRounds();renderCourses();renderCourseEditor();'
    if init_marker not in s:
        raise SystemExit('App initialization marker not found')
    s = s.replace(init_marker, init_marker + 'initRewardRoll();', 1)

# Fix the Rules tab Distance Limit chart by replacing the tab-separated text with
# a real HTML table. This prevents the multi-line headers from breaking apart and
# keeps every number directly under the correct disc-type column on desktop/mobile.
table_html = '''<div class="distance-chart"><table><thead><tr><th>Power</th><th>Putter (Speed 1-3)</th><th>Midrange (Speed 4-6)</th><th>Fairway (Speed 7-9)</th><th>Driver (Speed 10-14)</th></tr></thead><tbody><tr><td class="power-range">0 to 5</td><td>75</td><td>100</td><td>0</td><td>0</td></tr><tr><td class="power-range">6 to 10</td><td>125</td><td>150</td><td>175</td><td>200</td></tr><tr><td class="power-range">11 to 15</td><td>225</td><td>250</td><td>275</td><td>300</td></tr><tr><td class="power-range">16 to 20</td><td>325</td><td>350</td><td>375</td><td>400</td></tr><tr><td class="power-range">21 to 25</td><td>425</td><td>450</td><td>475</td><td>500</td></tr><tr><td class="power-range">26 to 30</td><td>525</td><td>550</td><td>575</td><td>600</td></tr><tr><td class="power-range">31 to 35</td><td>625</td><td>650</td><td>675</td><td>700</td></tr><tr><td class="power-range">36 to 40</td><td>725</td><td>750</td><td>775</td><td>800</td></tr><tr><td class="power-range">41 to 45</td><td>825</td><td>850</td><td>875</td><td>900</td></tr><tr><td class="power-range">46 to 50</td><td>925</td><td>950</td><td>975</td><td>100</td></tr></tbody></table></div>'''
anchor = "There are limits to distances you can throw, based on your Power and the type of disc you’re throwing, as seen in the following chart."
anchor_pos = s.find(anchor)
if anchor_pos != -1 and '<div class="distance-chart">' not in s[anchor_pos:s.find('CONTROL', anchor_pos)]:
    start = s.find('Power\tPutter', anchor_pos)
    if start == -1:
        start = s.find('Power', anchor_pos)
    end = s.find('CONTROL', start)
    if start != -1 and end != -1:
        s = s[:start] + table_html + '\\n' + s[end:]
        print('Distance Limit HTML table formatted successfully')
    else:
        print(f'Distance Limit table boundaries not found: start={start}, end={end}')
else:
    print('Distance Limit HTML table already present; leaving it intact')

# Style the chart as a true bordered grid, matching the supplied reference image.
distance_css = '''
.distance-chart{width:100%;overflow-x:auto;margin:14px 0 20px;-webkit-overflow-scrolling:touch}
.distance-chart table{width:100%;min-width:620px;border-collapse:collapse;table-layout:fixed}
.distance-chart th,.distance-chart td{border:1px solid #333;text-align:center;vertical-align:middle;padding:7px 5px;line-height:1.25}
.distance-chart th{font-weight:700;background:#f1f1f1;color:#111}
.distance-chart td{color:inherit}
.distance-chart .power-range{font-weight:600}
'''
if '.distance-chart table{' not in s:
    style_end = s.rfind('</style>')
    if style_end != -1:
        s = s[:style_end] + distance_css + s[style_end:]
    else:
        print('No style block found; chart table markup still added')

p.write_text(s, encoding='utf-8')
print('Reward Roll/source update completed')
