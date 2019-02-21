Feature: Load Data Lineage using API
  In order to load a data lineage CSV files are copied to a staging path

  Scenario: Load Lineage Data
    Given "app-admin" is authenticated
    When "app-admin" tries to load lineage data with following data:
      | File      | Id  | Name                  | Type           | Description                        | Select Hidden | Id Source | Id Target |
      | Resources | 1   | First Field           | Field          | This is First calculated field     |               |           |           |
      | Resources | 2   | Second Field          | Field          | This is Second calculated field    |               |           |           |
      | Resources | 3   | Third Field           | Field          | This is Third calculated field     |               |           |           |
      | Resources | 4   | Forth Field           | Field          | This is Fourth calculated field    |               |           |           |
      | Resources | 11  | First Transformation  | Transformation | This is the first transformation   |               |           |           |
      | Resources | 12  | Second Transformation | Transformation | This is the second transformation  |               |           |           |
      | Groups    | 101 | First Group           | System         | Our first group in simple example  | False         |           |           |
      | Groups    | 102 | Second Group          | System         | Our second group in simple example | False         |           |           |
      | Relations |     |                       | CONTAINS       |                                    |               | 101       | 1         |
      | Relations |     |                       | CONTAINS       |                                    |               | 101       | 11        |
      | Relations |     |                       | CONTAINS       |                                    |               | 102       | 2         |
      | Relations |     |                       | CONTAINS       |                                    |               | 102       | 3         |
      | Relations |     |                       | CONTAINS       |                                    |               | 102       | 4         |
      | Relations |     |                       | CONTAINS       |                                    |               | 102       | 12        |
      | Relations |     |                       | DEPENDS        |                                    |               | 3         | 12        |
      | Relations |     |                       | DEPENDS        |                                    |               | 12        | 4         |
      | Relations |     |                       | DEPENDS        |                                    |               | 12        | 2         |
      | Relations |     |                       | DEPENDS        |                                    |               | 2         | 11        |
      | Relations |     |                       | DEPENDS        |                                    |               | 11        | 1         |
    Then the system returns a result with code "Accepted"
    And the following files exist in the staging directory
      | Name                  |
      | nodes_groups.csv      |
      | nodes_resources.csv   |
      | rels_relations.csv    |
      | metadata_uploaded.log |
