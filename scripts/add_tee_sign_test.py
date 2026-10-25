from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
needle = "    if(c.description){const intro=document.createElement('div');intro.className='saved-round-detail';intro.style.margin='6px 0 10px';intro.textContent=c.description;d.appendChild(intro)}\n"
insert = needle + "    if(c.id==='builtin-first-course'){const teeSign=document.createElement('a');teeSign.className='secondary';teeSign.href='tee-signs/first-course-hole-1.svg';teeSign.target='_blank';teeSign.rel='noopener noreferrer';teeSign.textContent='View Hole 1 Tee Sign';teeSign.style.display='block';teeSign.style.textAlign='center';teeSign.style.textDecoration='none';teeSign.style.margin='6px 0 10px';d.appendChild(teeSign)}\n"

if 'tee-signs/first-course-hole-1.svg' in s:
    print('tee sign test already present')
    raise SystemExit(0)

if needle not in s:
    raise SystemExit('renderCourses insertion point not found')

p.write_text(s.replace(needle, insert, 1), encoding='utf-8')
print('updated index.html')
