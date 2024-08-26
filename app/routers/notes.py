from typing import List
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session
from .. import database, schemas, models, oauth2, utils

router = APIRouter(prefix="/notes", tags=["Notes"])


def create_user_friendly_suggestion_string(suggestions: list):
    return "\n".join([f"{', '.join(line[1])} вместо {line[0]}" for line in suggestions])


@router.post("/create", response_model=schemas.NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(database.get_db),
    current_user: schemas.UserOut = Depends(oauth2.get_current_user),
):
    """
    Method to create a new note.
    Body params:
    :title: required param that represents title of a note
    :contents: not required param that represents contents of a note
    """

    note_check_result = utils.check_for_spelling(title=note.title, contents=note.contents)
    if note_check_result != [[]]:
        suggestions = []
        for typo in note_check_result:
            correction = typo[0]
            user_word, corrected_words = correction["word"], correction["s"]
            suggestions.append((user_word, corrected_words))

        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=f"Вы опечатались. Возможно вы имели ввиду следующее?\n{create_user_friendly_suggestion_string(suggestions=suggestions)}",
        )

    note_dict = note.model_dump()
    note_dict.update({"creator_id": current_user.id})
    new_note = models.Note(**note_dict)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


@router.get("/", response_model=List[schemas.NoteOut], status_code=status.HTTP_200_OK)
def get_all_notes_by_user(
    db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(oauth2.get_current_user)
):
    """
    Method to get all logged user's notes
    """
    notes_query = db.query(models.Note).filter(models.Note.creator_id == current_user.id)
    notes = notes_query.all()

    return notes
