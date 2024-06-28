### short

- rename TestMixin as simply Mixin
- rename skeletor.test as skeletor.services
- tests to cover services
- single table/bucket/queue/userpool
- cognito to allow multiple users
 
### medium

- allow templates to sit in nested directory?
  - problem is having a flat directory is nice because then you can easily check fragments against template names

### thoughts

- adds templates/workers subdir for event, topic?
  - no I seem to remember I designed it assuming a flat directory structure
  - remember old template names

### done

- check for #{}
- run migrate_infra.py on templates
- refactor queue-event-worker event
- update init_env in scripts/create_handler.py
- table, bucket and queue event workers
- check pareto2 event types
- endpoint, event, timer, other?
