# Procejour Acceptance Test

Procejour is a Factory Acceptance Test server that provides a browser client for executing and gathering data from your shop floor.

## Auditing Model

_This is not implemented yet!_

A Procedure defines the set of steps, observations, and specifications to be performed. Each Datasheet is a performed instance of the Procedure. Procedures can be edited, but once a Datasheet is created, the latest Procedure is locked. Future edits to the Procedure are made on a later version of that Procedure.

```
Alpha Procedure (1)
| <- Edits made to Alpha Procedure
Alpha Procedure (1)
| -> Datasheet is created, references Alpha Procedure (1)
| <- Edits made to Alpha Procedure
Alpha Procedure (2)
| -> Another datasheet is created, references Alpha Procedure (2)
```

The exact procedure steps made for a given datasheet are always available, and a previous version of the procedure can be run if necessary.

All edits made to a Datasheet are tracked.
