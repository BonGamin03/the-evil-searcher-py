 
const DB_NAME = "evil_searcher";
const dbName = process.env.MONGO_INITDB_DATABASE || DB_NAME;

db = db.getSiblingDB(dbName);


db.createCollection("documents", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["doc_id", "title", "league", "url", "content"],
      properties: {
        doc_id: { bsonType: "int", description: "Incremental numeric ID (int32)" },
        title: { bsonType: "string" },
        league: { bsonType: "string" },
        url: { bsonType: "string" },
        content: { bsonType: "string" }
      },
      additionalProperties: true
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

 
db.documents.createIndex({ url: 1 }, { unique: true, name: "uniq_url" });
db.documents.createIndex({ doc_id: 1 }, { unique: true, name: "uniq_doc_id" });
db.documents.createIndex({ league: 1 }, { name: "idx_league" });

 
db.createCollection("counters");
 
db.counters.updateOne(
  { _id: "documents" },
  { $setOnInsert: { seq: 0 } },
  { upsert: true }
);

 