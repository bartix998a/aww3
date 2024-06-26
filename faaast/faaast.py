from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Form
import sqlite3

def add_tagDB(tag: str, cur):
    if cur.execute("SELECT * FROM tag").fetchone() == None:
        cur.execute('INSERT into tag(tag_id, tag) VALUES({}, \'{}\')'.format(1, tag))
    else:
        max = cur.execute("SELECT MAX(tag_id) FROM tag").fetchone()[0]
        cur.execute('INSERT into tag(tag_id, tag) VALUES(?, ?)', (str(max + 1), tag))

def add_relDB(pk_tag: int, pk_img: int, cur):
    if cur.execute("SELECT * FROM img_tag").fetchone() == None:
        cur.execute('INSERT into img_tag(rel_id, tag_id, img_id) VALUES(?, ?, ?)', ('1', str(pk_tag), str(pk_img)))
    else:
        max = cur.execute("SELECT MAX(rel_id) FROM img_tag").fetchone()[0]
        cur.execute('INSERT into img_tag(rel_id, tag_id, img_id) VALUES(?, ?, ?)', (str(max + 1), str(pk_tag), str(pk_img)))

worseImages = FastAPI()
@worseImages.get("/add/image/{title}", tags = ["add_image"])
async def add_image(title: str):
    """
    Funkcja dodaje obraz o tytule `title` do bazy danych obrazkow.
    **Argumenty:**

    * `titile` (float): Tytul dodawanego obrazka.

    **Wartość zwracana:**

    Słownik zawierający:

    * `success` - true jesli operacja zakonczyla sie powodzeniem false wpp.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    
    if cur.execute("SELECT * FROM image WHERE title=\'{}\'".format(title)).fetchone() != None:
        return {'success': False}
    
    if cur.execute("SELECT * FROM image").fetchone() == None:
        cur.execute('INSERT into image(img_id, title) VALUES({}, \'{}\')'.format(1, title))
    else:
        max = cur.execute('SELECT MAX(img_id) FROM image').fetchone()[0]
        cur.execute('INSERT into image(img_id, title) VALUES({}, \'{}\')'.format(max + 1, title))
    db.commit()
    return {'success': True}
        
@worseImages.get("/add/tag/{title}/{tag}")
async def add_tag(title: str, tag: str):
    """
    Funkcja przypisuje tag do obrazka o tytule `title`.
    **Argumenty:**

    * `title` (str): Tytul obrazka.
    * `tag` (str): Dodawany tag.

    **Wartość zwracana:**

    Słownik zawierający:

    * `success` - true jesli operacja zakonczyla sie powodzeniem false wpp.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    if cur.execute("SELECT * FROM tag WHERE tag=\'{}\'".format(tag)).fetchone() == None:
        add_tagDB(tag, cur)
    pk_tag = cur.execute("SELECT tag_id FROM tag WHERE tag=\'{}\'".format(tag)).fetchone()[0]
    pk_img = cur.execute("SELECT img_id FROM image WHERE title=\'{}\'".format(title)).fetchone()[0]
    if cur.execute("SELECT * FROM img_tag WHERE tag_id=? AND img_id=?", (str(pk_tag), str(pk_img))).fetchone() == None:
        add_relDB(pk_tag, pk_img, cur)
    db.commit()
    return {'success': True}

@worseImages.get("/tags")
async def list_tags():
    """
    Funkcja zwraca slownik w ktorym pod nazwa tagu jest wypisana liczba obrazkow z tym tagiem.
    **Wartość zwracana:**

    Słownik w postaci:

    * `dict[str] = int`, gdzie `int` to liczba obrazkow posiadajacych tag   tytule `str`.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    tags = cur.execute("SELECT A.tag, COUNT(C.title) FROM tag A, img_tag B, image C WHERE A.tag_id = B.tag_id AND B.img_id = C.img_id GROUP BY A.tag").fetchall()
    result = {}
    for tup in tags:
        result[tup[0]] = tup[1]
    return result
    
@worseImages.get("/images")
async def list_images():
    """
    Funkcja zwraca pary w postaci `tytul_obrazka`, `lista tagow przypisanych do obrazka`.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    tags = cur.execute("SELECT C.title, A.tag FROM tag A, img_tag B, image C WHERE A.tag_id = B.tag_id AND B.img_id = C.img_id").fetchall()
    result = {}
    for tup in tags:
        if not (tup[0] in result):
            result[tup[0]] = [tup[1]]
        else:
            result[tup[0]].append(tup[1])
    return result
    
@worseImages.get("/images/{tag}")
async def list_images(tag: str):
    """
    Funkcja listuje wszystkie obrazki przypisane do tagu `tag`
    **Argumenty:**

    * `tag` (str): Nazwa tagu jak wyzej.

    **Wartość zwracana:**

    slownik zawierajcy w kluczach od `'1'` do `'i'` nazwe `i`-tego obrazka.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    tags = cur.execute("SELECT C.title FROM tag A, img_tag B, image C WHERE A.tag_id = B.tag_id AND B.img_id = C.img_id and A.tag = \'" + tag +'\'').fetchall()
    result = {}
    tmp = len(tags)
    for i in range(1, tmp + 1):
        result[str(i)] = tags.pop()
    return result

class Del_class(BaseModel):
    images: list[str]

@worseImages.post("/images/del")
async def del_images(del_c: Del_class):
    """
    Funkcja usuwa obrazki zapisane w `images`. Argumenty przyjmowane sa w postaci jsona.
    **Argumenty:**

    * `images` list[str]: Lista obrazkow do usuniecia.

    **Wartość zwracana:**

    Słownik zawierający:

    * `success` - true jesli operacja zakonczyla sie powodzeniem false wpp.
    """
    db = sqlite3.connect("fast.db")
    cur = db.cursor()
    for title in del_c.images:
        pk_img = cur.execute("SELECT img_id FROM image WHERE title=\'" + title + '\'').fetchone()[0]
        cur.execute('DELETE FROM img_tag WHERE img_id = ?', (str(pk_img)))
        cur.execute('DELETE FROM image WHERE img_id = ?', (str(pk_img)))
    cur.execute('DELETE FROM tag  WHERE NOT EXISTS (SELECT * FROM img_tag B WHERE tag.tag_id = B.tag_id)')
    db.commit()
    return {"success": True}