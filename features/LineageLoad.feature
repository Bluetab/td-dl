Feature: Load Data Lineage using API
  In order to load a data lineage three bulk data groups will be given:
    Resources:
      | Field       | Example                    |
      | Id          | 4                          |
      | Name        | National Audience          |
      | Type        | Field                      |
      | Description | This is a calculated field |
    Groups:
      | Field       | Example                 |
      | Id          | 104                     |
      | Name        | SAS Base                |
      | Type        | System                  |
      | ShowTree    | True                    |
      | Description | All SW developed in SAS |
    Relations (Contains and Depends):
      | Field     | Example |
      | Id Source | 104     |
      | Id Target | 4       |
      | Type      | Groups  |

  Scenario: Load Lineage Data
    When "app-admin" tries to load lineage data with following data:
      | File        | Id  | Name                  | Type           | Description                        | Showtree | Id Source | Id Target |
      | Resources   | 1   | First Field           | Field          | This is First calculated field     |          |           |           |
      | Resources   | 2   | Second Field          | Field          | This is Second calculated field    |          |           |           |
      | Resources   | 3   | Third Field           | Field          | This is Third calculated field     |          |           |           |
      | Resources   | 4   | Forth Field           | Field          | This is Fourth calculated field    |          |           |           |
      | Resources   | 11  | First Transformation  | Transformation | This is the first transformation   |          |           |           |
      | Resources   | 12  | Second Transformation | Transformation | This is the second transformation  |          |           |           |
      | Groups      | 101 | First Group           | System         | Our first group in simple example  | True     |           |           |
      | Groups      | 102 | Second Group          | System         | Our second group in simple example | True     |           |           |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 1         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 11        |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 2         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 3         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 4         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 3         | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 4         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 2         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 2         | 11        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 11        | 1         |
    Then the system returns a result with code "Created"
    And "app-admin" is able to view following "lineage" for Resource with Id "3" and top level Group type "System"
      | Id  | Name                  | Type           | Description                        | Contains | Depends |
      | 3   | Third Field           | Field          | This is Third calculated field     |          | 12      |
      | 12  | Second Transformation | Transformation | This is the second transformation  |          | 4,2     |
      | 4   | Forth Field           | Field          | This is Fourth calculated field    |          |         |
      | 2   | Second Field          | Field          | This is Second calculated field    |          | 11      |
      | 11  | First Transformation  | Transformation | This is the first transformation   |          | 1       |
      | 1   | First Field           | Field          | This is First calculated field     |          |         |
      | 101 | First Group           | System         | Our first group in simple example  | 1,11     |         |
      | 102 | Second Group          | System         | Our second group in simple example | 2,3,4,12 | 101     |

  Scenario: Basic impact analysis
    Given following lineage data has been already loaded:
      | File        | Id  | Name                  | Type           | Description                        | Showtree | Id Source | Id Target |
      | Resources   | 1   | First Field           | Field          | This is First calculated field     |          |           |           |
      | Resources   | 2   | Second Field          | Field          | This is Second calculated field    |          |           |           |
      | Resources   | 3   | Third Field           | Field          | This is Third calculated field     |          |           |           |
      | Resources   | 4   | Forth Field           | Field          | This is Fourth calculated field    |          |           |           |
      | Resources   | 11  | First Transformation  | Transformation | This is the first transformation   |          |           |           |
      | Resources   | 12  | Second Transformation | Transformation | This is the second transformation  |          |           |           |
      | Groups      | 101 | First Group           | System         | Our first group in simple example  | True     |           |           |
      | Groups      | 102 | Second Group          | System         | Our second group in simple example | True     |           |           |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 1         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 11        |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 2         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 3         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 4         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 3         | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 4         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 2         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 2         | 11        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 11        | 1         |
    When "app-admin" tries to get the "impact" analysis for Resource with Id "1" and top level Group type "System"
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
    Given following lineage data has been already loaded:
      | File        | Id  | Name                  | Type           | Description                        | Showtree | Id Source | Id Target |
      | Resources   | 1   | First Field           | Field          | This is First calculated field     |          |           |           |
      | Resources   | 2   | Second Field          | Field          | This is Second calculated field    |          |           |           |
      | Groups      | 11  | First Transformation  | System         | This is the first transformation   | True     |           |           |
      | Groups      | 12  | Second Transformation | System         | This is the second transformation  | True     |           |           |
      | Groups      | 101 | First Group           | System         | Our first group in simple example  | True     |           |           |
      | Groups      | 102 | Second Group          | System         | Our second group in simple example | True     |           |           |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 1         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 11        |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 2         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 2         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 2         | 11        |
    When "app-admin" tries to list Groups with a contains relation with Group Id "101"
    Then he receives following nodes list:
      | Id  | Name                  | Type           | Description                        |
      | 1   | First Field           | Field          | This is First calculated field     |
      | 11  | First Transformation  | System         | This is the first transformation   |

  Scenario: List top groups
    Given following lineage data has been already loaded:
      | File        | Id  | Name                  | Type           | Description                        | Showtree | Id Source | Id Target |
      | Resources   | 1   | First Field           | Field          | This is First calculated field     |          |           |           |
      | Resources   | 2   | Second Field          | Field          | This is Second calculated field    |          |           |           |
      | Groups      | 11  | First Transformation  | System         | This is the first transformation   | True     |           |           |
      | Groups      | 12  | Second Transformation | System         | This is the second transformation  | True     |           |           |
      | Groups      | 101 | First Group           | System         | Our first group in simple example  | True     |           |           |
      | Groups      | 102 | Second Group          | System         | Our second group in simple example | True     |           |           |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 1         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 101       | 11        |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 2         |
      | Relations   |     |                       | CONTAINS       |                                    |          | 102       | 12        |
      | Relations   |     |                       | DEPENDS        |                                    |          | 12        | 2         |
      | Relations   |     |                       | DEPENDS        |                                    |          | 2         | 11        |
    When "app-admin" tries to list top Groups
    Then he receives following nodes list:
      | Id  | Name                  | Type           | Description                        |
      | 101 | First Group           | System         | Our first group in simple example  |
      | 102 | Second Group          | System         | Our second group in simple example |
