from __future__ import annotations

from uuid import uuid4

from reference_results_model import (
    SessionLocal,
    ReferenceResult,
    ReferenceStatus,
    init_db,
)


def run():
    init_db()

    session = SessionLocal()

    try:
        record = ReferenceResult(
            batch_id=uuid4(),
            ref_type="document_id",
            ref_value="doc_404",
            status=ReferenceStatus.invalid,
            error_code="NOT_FOUND",
            message="Referenced document does not exist.",
            source="user_input",
        )

        session.add(record)
        session.commit()

        print("INSERT OK")
        print(f"id={record.id} status={record.status}")

    except Exception as e:
        session.rollback()
        raise

    finally:
        session.close()


if __name__ == "__main__":
    run()
