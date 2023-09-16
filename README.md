# Users-microservice

[![codecov](https://codecov.io/gh/SnapMsg-Inc/g1.users.api/graph/badge.svg?token=ZAMM2TX3MT)](https://codecov.io/gh/SnapMsg-Inc/g1.users.api)

A microservice component for the SnapMsg API.

## Getting Started

### Dependencies

Before you begin, ensure you have met the following requirements, which are also listed in the `requirements.txt` file:

- **FastAPI:** `0.103.1`
- **Uvicorn:** `0.23.2`
- **DataDog:** `0.47.0`
- **Pydantic:** `2.3.0`
- **SQLAlchemy:** `2.0.20`
- **Psycopg2:** `2.9.7`
- **New Relic:** `9.0.0`
- **Pytest:** `7.2.1`
- **HTTPX:** `0.23.3`
- **Docker:** `1.0`


### Executing program

To run the program, execute the following command:

```sh
uvicorn main:app --host 0.0.0.0 --port 3000
```

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.

## Acknowledgments

Inspiration, code snippets, etc.:

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Okteto](https://okteto.com/docs/)
- [Taller de Programación 2](https://taller-de-programacion-2.github.io/)
