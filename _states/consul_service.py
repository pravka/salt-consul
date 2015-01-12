# -*- coding: utf-8 -*-
'''
Management of consul server
==========================

.. versionadded:: 2014.7.0

:depends:   - consul Python module
:configuration: See :py:mod:`salt.modules.consul` for setup instructions.

.. code-block:: yaml

    service_in_consul:
        consul_service.present:
            - name: foo
            - port: 6969
            - script: nc -z localhost 6969
            - interval: 10s

    service_not_in_consul:
        consul_service.absent:
            - name: foo

'''

__virtualname__ = 'consul_service'


def __virtual__():
    '''
    Only load if the consul module is in __salt__
    '''
    if 'consul.key_put' in __salt__:
        return __virtualname__
    return False


def present(name, service_id=None, port=None, tags=None, script=None, interval=None, ttl=None):
    '''
    Ensure the named service is present in Consul

    name
        consul service to manage

    service_id
        alternative service id

    port
        service port

    tags
        list of tags to associate with this service

    script + interval
        path to script for health checks, paired with invocation interval

    ttl
        length of time a service should remain healthy before being updated
        note: if this is specified, script + interval must not be used        
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service "%s" updated' % (name)}

    if not __salt__['consul.service_get'](name):
        __salt__['consul.service_register'](name, service_id, port, tags, script, interval, ttl)
        ret['changes'][name] = 'Service created'
        ret['comment'] = 'Service "%s" created' % (name)

    else:
        __salt__['consul.service_register'](name, service_id, port, tags, script, interval, ttl)
    
    return ret


def absent(name):
    '''
    Ensure the named service is absent in Consul

    name
        consul service to manage
        
    '''
    ret = {'name': name,
           'changes': {},
           'result': True,
           'comment': 'Service "%s" removed' % (name)}

    if not __salt__['consul.service_get'](name):
        ret['comment'] = 'Service "%s" already absent' % (name)

    else:
        __salt__['consul.service_deregister'](name)
    
    return ret
    