from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DATABASE_URL = "sqlite:///./veritext.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


# =========================================================
# CREATE TABLES + SAFE DATABASE MIGRATION
# =========================================================

def create_tables():

    # Create all new tables
    Base.metadata.create_all(bind=engine)

    # -----------------------------------------------------
    # SAFE MIGRATION:
    # Add assignment_id to existing submissions table
    # if it does not already exist.
    # -----------------------------------------------------

    with engine.connect() as connection:

        # Check whether submissions table exists
        result = connection.execute(
            text(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table'
                AND name='submissions'
                """
            )
        )

        submissions_exists = result.fetchone() is not None

        if submissions_exists:

            # Get existing columns
            result = connection.execute(
                text("PRAGMA table_info(submissions)")
            )

            columns = result.fetchall()

            column_names = [
                column[1]
                for column in columns
            ]

            # Add the new column only if required
            migrated = False
            if "student_record_id" not in column_names:

                connection.execute(
                    text(
                        """
                        ALTER TABLE submissions
                        ADD COLUMN student_record_id INTEGER
                        """
                    )
                )

                connection.commit()
                migrated = True

                print(
                    "Database migration completed: "
                    "student_record_id added to submissions."
                )

            if "assignment_id" not in column_names:
                connection.execute(
                    text(
                        """
                        ALTER TABLE submissions
                        ADD COLUMN assignment_id INTEGER
                        """
                    )
                )
                connection.commit()
                migrated = True
                print(
                    "Database migration completed: "
                    "assignment_id added to submissions."
                )

            if not migrated:
                print(
                    "Database already up to date."
                )

            connection.execute(
                text(
                    """
                    UPDATE submissions
                    SET student_record_id = (
                        SELECT MIN(students.id)
                        FROM students
                        WHERE lower(trim(students.name))
                            = lower(trim(submissions.student_name))
                    )
                    WHERE student_record_id IS NULL
                    AND (
                        SELECT COUNT(*)
                        FROM students
                        WHERE lower(trim(students.name))
                            = lower(trim(submissions.student_name))
                    ) = 1
                    """
                )
            )
            connection.execute(
                text(
                    """
                    UPDATE submissions
                    SET assignment_id = (
                        SELECT MIN(assignments.id)
                        FROM assignments
                        JOIN students
                            ON students.section_id = assignments.section_id
                        WHERE students.id = submissions.student_record_id
                        AND lower(trim(assignments.title))
                            = lower(trim(submissions.assignment_title))
                        AND lower(trim(assignments.subject))
                            = lower(trim(submissions.subject))
                    )
                    WHERE assignment_id IS NULL
                    AND student_record_id IS NOT NULL
                    AND (
                        SELECT COUNT(*)
                        FROM assignments
                        JOIN students
                            ON students.section_id = assignments.section_id
                        WHERE students.id = submissions.student_record_id
                        AND lower(trim(assignments.title))
                            = lower(trim(submissions.assignment_title))
                        AND lower(trim(assignments.subject))
                            = lower(trim(submissions.subject))
                    ) = 1
                    """
                )
            )
            connection.commit()

        else:

            print(
                "Submissions table does not exist yet."
            )