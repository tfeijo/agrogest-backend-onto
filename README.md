# Agrogest - ontology backend API

## Routes

**City**
- /cities (GET)
- /cities/id (GET)
- /states/<state-identifier>/cities (GET)
- /biomes/<biome-identifier>/cities (GET)

**State**
- /states (GET)
- /states/id (GET)

**Biome**
- /biomes (GET)
- /biomes/id (GET)

**Farm**
- /lands (GET,POST)
- /lands/id (GET)
## 

## List all cities

**Definition**

`GET /cities`

**Response**

- `200 OK` on success

```json
[
    {
    "id": 2972,
    "name": "ABADIA DE GOIÁS",
    "fiscal_module": 24,
    "state": {
      "id": 25,
      "name": "Goiás"
    },
    "biomes": [
      {
        "id": 1,
        "name": "Cerrado"
      }
    ]
  },
]
```
## 

## Lookup city details

`GET /cities/<identifier>`

**Response**

- `404 Not Found` if the city does not exist
- `200 OK` on success
```json
[
    {
    "id": 2972,
    "name": "ABADIA DE GOIÁS",
    "fiscal_module": 24,
    "state": {
      "id": 25,
      "name": "Goiás"
    },
    "biomes": [
      {
        "id": 1,
        "name": "Cerrado"
      }
    ]
  },
]
```
## 

## Lookup city by state

**Definition**

`GET /states/<state-identifier>/cities`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
[
  {
    "id": 49,
    "name": "AMPARO DE SÃO FRANCISCO"
  },
  {
    "id": 430,
    "name": "CANHOBA"
  },
  {
    "id": 276,
    "name": "AREIA BRANCA"
  },
]

```
## 

## Lookup city by biome

**Definition**

`GET /biomes/<biome-identifier>/cities`

**Response**

- `404 Not Found` if the device does not exist
- `200 OK` on success

```json
[
  {
    "id": 1,
    "name": "ABAETÉ"
  },
  {
    "id": 6,
    "name": "ABREULÂNDIA"
  },
]

```
## 

## List all states

**Definition**

`GET /states`

**Response**

- `200 OK` on success

```json
[
  {
    "id": 2,
    "name": "Acre",
    "uf": "AC"
  },
  {
    "id": 14,
    "name": "Alagoas",
    "uf": "AL"
  },
]
```
## 

## Lookup state details

`GET /states/<state-identifier>`

**Response**

- `404 Not Found` if the state does not exist
- `200 OK` on success
```json
{
  "id": 1,
  "name": "Rondônia",
  "uf": "RO",
  "createdAt": "2020-04-29T18:38:59.741Z",
  "updatedAt": "2020-04-29T18:38:59.741Z"
}
```
## 

## List all biomes

**Definition**

`GET /biomes`

**Response**

- `200 OK` on success

```json
[
  {
    "id": 1,
    "name": "Cerrado"
  },
  {
    "id": 2,
    "name": "Caatinga"
  },
]
```
## 

## Lookup biomes details

`GET /biomes/<biome-identifier>`

**Response**

- `404 Not Found` if the biomes does not exist
- `200 OK` on success
```json
{
  "id": 1,
  "name": "Cerrado"
}
```
## 

## List all Farms

**Definition**

`GET /lands`

**Response**

- `200 OK` on success

```json
[
  {
    "id": 10,
    "installation_id": "512e7afe-f136-41bb-8ffa-5c88dc40f00f",
    "hectare": 601,
    "licensing": true,
    "city": {
      "id": 1,
      "name": "ABAETÉ",
      "state": {
        "id": 17,
        "name": "Minas Gerais",
        "uf": "MG"
      },
      "biomes": [
        {
          "id": 1,
          "name": "Cerrado"
        }
      ]
    },
    "size": {
      "id": 3,
      "name": "Grande Propriedade"
    }
  },
  {
    "id": 11,
    "installation_id": "90778c68-e126-46f2-9166-925e3fecfffe",
    "hectare": 601,
    "licensing": true,
    "city": {
      "id": 1,
      "name": "ABAETÉ",
      "state": {
        "id": 17,
        "name": "Minas Gerais",
        "uf": "MG"
      },
      "biomes": [
        {
          "id": 1,
          "name": "Cerrado"
        }
      ]
    },
    "size": {
      "id": 3,
      "name": "Grande Propriedade"
    }
  },
]
```
## 

## Lookup lands details

`GET /lands/<land-identifier>`

**Response**

- `404 Not Found` if the land does not exist
- `200 OK` on success
```json
{
  "id": 40,
  "installation_id": "f36a253e-7760-421b-a909-30b96b6287c8",
  "hectare": 15,
  "licensing": true,
  "city": {
    "id": 2157,
    "name": "ABDON BATISTA",
    "state": {
      "id": 22,
      "name": "Santa Catarina",
      "uf": "SC"
    },
    "biomes": [
      {
        "id": 5,
        "name": "Mata Atlântica"
      }
    ]
  },
  "size": {
    "id": 1,
    "name": "Pequena Propriedade"
  }
}
```
## 



## Creating a Farm
**Definition**

`POST /lands`

**Arguments**

- `"installation_id":null` an unique Id generated from API
- `"hectare":integer` a Farm size hectare number 
- `"city_id":integer` City id where Farm belongs
- `"licensing":boolean` True if Farm has licensing environmental

``` json
{
	"installation_id": null,
	"hectare": 601,
	"city_id": 1,
	"licensing": true
}
```

**Response**

- `201 Created` on success

```json
{
  "id": 11,
  "installation_id": "90778c68-e126-46f2-9166-925e3fecfffe",
  "hectare": 601,
  "city_id": 1,
  "licensing": true,
  "size_id": 3,
}
```
## 