
# Neo4j + Neosemantics (n10s) + OWL Import

## 1. Pull the Neo4j Docker image

```bash
docker pull neo4j:latest
```

## 2. Run the Neo4j container

```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/test123 \
  -v $HOME/neo4j/data:/data \
  neo4j:latest
```

## 3. Copy plugins and ontology files into the container

```bash
docker cp neosemantics-5.20.0.jar neo4j:/var/lib/neo4j/plugins/

docker cp bt.owl neo4j:/var/lib/neo4j/import/bt.owl
```

## 4. Run Neo4j with n10s plugin enabled

```bash
docker run -d --name neo4j -p7474:7474 -p7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["n10s"]' \
  neo4j:5
```

## 5. Initialize n10s in Neo4j

```bash
docker exec -it neo4j cypher-shell -u neo4j -p password "CALL n10s.graphconfig.init();"
```

## 6. Import OWL file into Neo4j

```bash
docker exec -it neo4j cypher-shell -u neo4j -p password \
  "CALL n10s.rdf.import.fetch('file:///var/lib/neo4j/import/bt.owl','Turtle');"
```

## 7. Access Neo4j Browser

Open: [http://localhost:7474/browser/preview/](http://localhost:7474/browser/preview/)

---

### Example Cypher Queries

1. Remove `:Resource` label
    

```cypher
MATCH (n:Resource)
REMOVE n:Resource
```

2. Simplify node names from `uri`
    

```cypher
MATCH (n)
WHERE n.uri IS NOT NULL
WITH n,
  CASE
    WHEN n.uri CONTAINS '#' THEN split(n.uri, '#')[-1]
    ELSE split(n.uri, '/')[-1]
  END AS simple_name
SET n.name = simple_name
```
