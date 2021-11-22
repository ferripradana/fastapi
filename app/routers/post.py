from requests import status_codes
from sqlalchemy.sql.expression import text
from .. import models, schemas, oauth2
from fastapi import  Response, status, Depends, APIRouter
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db
from typing import List, Optional

from fastapi_pagination import Page
from fastapi_pagination.paginator import paginate

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=Page[schemas.Post])
@router.get("/", response_model=Page[schemas.PostOut])
def posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), search: Optional[str] = "", sort_by: str="id", sort_dir: str="asc"):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    '''
    posts = (db.query(models.Post).filter(models.Post.owner_id == current_user.id)
                                  .filter(models.Post.title.contains(search))
                                  .order_by(text(sort_by+" "+sort_dir))
                                  #.limit(limit).offset((page-1)*limit)
                                  .all())   
    '''
    posts = (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                .filter(models.Post.owner_id == current_user.id)
                .filter(models.Post.title.contains(search))
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                .group_by(models.Post.id)
                .order_by(text(sort_by+" "+sort_dir))
                .all()
    )

    return paginate(posts)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPost(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)): 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #     (post.title, post.content, post.published)
    # )
    # conn.commit()
    # new_post = cursor.fetchone()
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    # new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id =  %s """, (str(id)))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).filter(models.Post.id == id).first()
    post = (
            db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
                .filter(models.Post.owner_id == current_user.id)
                .filter(models.Post.id == id)
                .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
                .group_by(models.Post.id)
                .first()
    )
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,  db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s returning *""",(str(id)))
    # deleted = cursor.fetchone()
    # conn.commit()

    deleted = db.query(models.Post).filter(models.Post.id == id)

    if deleted.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} does not exist")

    if deleted.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not authorized to perform the action")

    deleted.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) 


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),  current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts set title= %s, content= %s, published = %s where id= %s returning *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query =  db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesnot exists")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not authorized to perform the action")


    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

#title str, content str , category, Bool published