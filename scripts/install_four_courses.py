from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# The four courses are already installed. Rebuild their order every deployment.
if "id:'builtin-tdg-middle-school'" not in s:
    raise SystemExit('Four TDG courses are not installed yet.')

old = "savedCourses=savedCourses.filter(c=>c.id!=='builtin-18'&&c.id!=='builtin-first-course'&&c.id!=='builtin-everyones-favorite-local'&&c.id!=='builtin-legendary-local'&&c.id!=='builtin-tdg-middle-school'&&c.id!=='builtin-tdg-high-school'&&c.id!=='builtin-tdg-university'&&c.id!=='builtin-tdg-world-champion').map(c=>c.id==='builtin-9'?{...c,name:'TDG Elementary'}:c);savedCourses.unshift(tdgWorldChampionCourse);savedCourses.unshift(tdgUniversityCourse);savedCourses.unshift(tdgHighSchoolCourse);savedCourses.unshift(tdgMiddleSchoolCourse);savedCourses.unshift(legendaryLocalCourse);savedCourses.unshift(favoriteLocalCourse);savedCourses.unshift(firstCourse);localStorage.setItem('tinyCourses',JSON.stringify(savedCourses));"
new = "savedCourses=savedCourses.filter(c=>c.id!=='builtin-18'&&c.id!=='builtin-first-course'&&c.id!=='builtin-everyones-favorite-local'&&c.id!=='builtin-legendary-local'&&c.id!=='builtin-9'&&c.id!=='builtin-tdg-middle-school'&&c.id!=='builtin-tdg-high-school'&&c.id!=='builtin-tdg-university'&&c.id!=='builtin-tdg-world-champion');savedCourses.unshift(tdgWorldChampionCourse);savedCourses.unshift(tdgUniversityCourse);savedCourses.unshift(tdgHighSchoolCourse);savedCourses.unshift(tdgMiddleSchoolCourse);savedCourses.unshift(tdgElementaryCourse);savedCourses.unshift(legendaryLocalCourse);savedCourses.unshift(favoriteLocalCourse);savedCourses.unshift(firstCourse);localStorage.setItem('tinyCourses',JSON.stringify(savedCourses));"
if old not in s:
    raise SystemExit('Course save/unshift marker not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('Reordered TDG school progression: Elementary, Middle School, High School, University, World Champion.')