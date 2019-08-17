## Workers Mircoservice
This is a simple CRUD microservice to manage workers in a team.

#### Features
- A member has a name and a type the late one can be an employee or a contractor - if it's a contractor, the duration of the contract needs to be saved (as contractEnd, a date in RFC3339), and if it's an employee we need to store their role, for instance: Software Engineer, Project Manager and so on.
- A member can be tagged, for instance: C#, Angular, General Frontend, Seasoned Leader and so on. (Tags will likely be used as filters later, so keep that in mind)

#### API Documentation

The service uses standard HTTP verbs to the endpoint `/worker`, Please take a look at `tests/acceptance` for details.

#### How to Run
You need `make` and `docker-compose` to run the service, e.g.:

    `make run`

To run the tests, you need additionally pytest:

    `make test`

### Roadmap

1. add an endpoint to query workers based on name, type, tags and contractEnd
2. add unit and integration tests
3. put nginx in front of the api
