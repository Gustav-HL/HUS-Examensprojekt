BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Documents" (
    "doc_id" TEXT,
    "title"  TEXT,
    "file_path"  TEXT,
    "file_type"  TEXT,
    "author"  TEXT,
    "creator"   TEXT,
    "creation_date" TEXT,
    "modification_date" TEXT,
    "keywords" TEXT,
    PRIMARY KEY("doc_id")
);
CREATE TABLE IF NOT EXISTS "Chunks" (
	"chunk_id" TEXT,
	"doc_id" TEXT,
	"chunk_index" INTEGER,
	"text_content" TEXT,
	"entities" TEXT,
	PRIMARY KEY("chunk_id"),
	FOREIGN KEY("doc_id") REFERENCES "Documents"("doc_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Vectors" (
	"chunk_id"	TEXT,
	"vector"	BLOB,
	PRIMARY KEY("chunk_id"),
	FOREIGN KEY("chunk_id") REFERENCES "Chunks"("chunk_id") ON DELETE CASCADE
);
COMMIT;
