Disable AppArmor
----------------

The rules for app armor is enforced for rsyslog so it must be disabled:

`aa-disable rsyslogd`

and check with

`aa-status`

Modules
-------

Load modules

```
module(load="mmexternal")
```
