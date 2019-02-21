Feature: Query Data Lineage using API
      In order to execute data lineage queries, the following data is loaded in Neo4J:
      Groups:
      | :LABEL | description                        | external_id:ID | name         | select_hidden:boolean | type   |
      | Group  | Our first group in simple example  | 101            | First Group  | False                 | System |
      | Group  | Our second group in simple example | 102            | Second Group | False                 | System |
      | Group  | A child groud                      | 103            | Child Group  | False                 | Schema |
      Resources:
      | :LABEL   | description                       | external_id:ID | name                  | type           |
      | Resource | This is First calculated field    | 1              | First Field           | Field          |
      | Resource | This is Second calculated field   | 2              | Second Field          | Field          |
      | Resource | This is Third calculated field    | 3              | Third Field           | Field          |
      | Resource | This is Fourth calculated field   | 4              | Forth Field           | Field          |
      | Resource | This is the first transformation  | 11             | First Transformation  | Transformation |
      | Resource | This is the second transformation | 12             | Second Transformation | Transformation |
      Relations (Contains and Depends):
      | :START_ID | :END_ID | :TYPE    |
      | 101       | 1       | CONTAINS |
      | 101       | 11      | CONTAINS |
      | 101       | 103     | CONTAINS |
      | 102       | 2       | CONTAINS |
      | 102       | 3       | CONTAINS |
      | 102       | 4       | CONTAINS |
      | 102       | 12      | CONTAINS |
      | 3         | 12      | DEPENDS  |
      | 12        | 4       | DEPENDS  |
      | 12        | 2       | DEPENDS  |
      | 2         | 11      | DEPENDS  |
      | 11        | 1       | DEPENDS  |

  Scenario: Basic impact analysis
    Given "app-admin" is authenticated
    When "app-admin" tries to get the "lineage" analysis for Resource with Id "1" and top level Group type "System"
    Then he receives following lineage information:
      | Id  | Name                  | Type           | Description                        | Contains | Depends |
      | 1   | First Field           | Field          | This is First calculated field     |          | 11      |
      | 11  | First Transformation  | Transformation | This is the first transformation   |          | 2       |
      | 2   | Second Field          | Field          | This is Second calculated field    |          | 12      |
      | 12  | Second Transformation | Transformation | This is the second transformation  |          | 3       |
      | 3   | Third Field           | Field          | This is Third calculated field     |          |         |
      | 101 | First Group           | System         | Our first group in simple example  | 1,11     | 102     |
      | 102 | Second Group          | System         | Our second group in simple example | 2,3,4,12 |         |

  Scenario: Get a list of nodes with a contains relation
    Given "app-admin" is authenticated
    When "app-admin" tries to list Resources with a contains relation with Group Id "101"
    Then he receives following nodes list:
      | Id | Name                 | Type           | Description                      |
      | 1  | First Field          | Field          | This is First calculated field   |
      | 11 | First Transformation | Transformation | This is the first transformation |

  Scenario: List top groups
    Given "app-admin" is authenticated
    When "app-admin" tries to list top Groups
    Then he receives following nodes list:
      | Id  | Name         | Type   | Description                        |
      | 101 | First Group  | System | Our first group in simple example  |
      | 102 | Second Group | System | Our second group in simple example |
