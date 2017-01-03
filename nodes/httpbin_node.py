#!/usr/bin/env python
from __future__ import absolute_import

import json

"""
 A very simple echo ROS node class.
 - echo from topic to echo_topic
 - echo service
"""

try:

    import roslib
    import rospy
    import std_msgs.msg as std_msgs
    import pyros_schemas

    from pyros_rosclient.msg import HttpStatusCode, HttpRequestHeaders, HttpResponseHeaders, HttpbinGetArgs, HttpbinPostArgs, HttpbinPostBody, HttpbinPostBody2
    from pyros_rosclient.srv import HttpbinIp, HttpbinUserAgent, HttpbinHeaders, HttpbinGet, HttpbinPostJson, HttpbinPostForm, HttpbinPostFiles
    import pyros_msgs.opt_as_array  # This will duck punch the standard message type initialization code.

except ImportError:
    # Because we need to access Ros message types here (from ROS env or from virtualenv, or from somewhere else)
    import pyros_setup
    # We rely on default configuration in the environment to point us ot the proper distro and workspace
    pyros_setup.configurable_import().configure().activate()

    import roslib
    import rospy
    import std_msgs.msg as std_msgs
    import pyros_schemas

    from pyros_rosclient.msg import HttpStatusCode, HttpRequestHeaders, HttpResponseHeaders, HttpbinGetArgs, HttpbinPostArgs, HttpbinPostBody, HttpbinPostBody2
    from pyros_rosclient.srv import HttpbinIp, HttpbinUserAgent, HttpbinHeaders, HttpbinGet, HttpbinPostJson, HttpbinPostForm, HttpbinPostFiles
    import pyros_msgs.opt_as_array  # This will duck punch the standard message type initialization code.

# patching messages types with optional fields
pyros_msgs.opt_as_array.duck_punch(HttpRequestHeaders, [
    'User_Agent',
    'Accept',
    'Accept_Encoding',
    'Accept_Language',
    'Host',
    'Referer',
    'Upgrade_Insecure_Requests',
])
pyros_msgs.opt_as_array.duck_punch(HttpbinGetArgs, ['argopt'])
pyros_msgs.opt_as_array.duck_punch(HttpbinGet._request_class, ['headers'])

pyros_msgs.opt_as_array.duck_punch(HttpbinPostArgs, ['argopt'])
pyros_msgs.opt_as_array.duck_punch(HttpbinPostJson._request_class, ['headers'])
pyros_msgs.opt_as_array.duck_punch(HttpbinPostArgs, ['argopt'])
pyros_msgs.opt_as_array.duck_punch(HttpbinPostBody, ['testoptitem'])
pyros_msgs.opt_as_array.duck_punch(HttpbinPostBody2, ['subtestoptstring', 'subtestoptint', 'subtestoptfloat'])

import marshmallow
import requests

##########
# Services
##########


import requests
import rostful_requests


@rostful_requests.with_service_schemas(HttpbinIp)
def httpbin_ip_callback(data, data_dict, errors):
    return requests.get('http://httpbin.org/ip', data=data_dict)


@rostful_requests.with_service_schemas(HttpbinUserAgent)
def httpbin_useragent_callback(data, data_dict, errors):
    return requests.get('http://httpbin.org/user-agent', data=data_dict)


@rostful_requests.with_service_schemas(HttpbinHeaders)
def httpbin_headers_callback(data, data_dict, errors):
    return requests.get('http://httpbin.org/headers', headers=data_dict.get('headers', {}))


@rostful_requests.with_service_schemas(HttpbinGet)
def httpbin_get_callback(data, data_dict, errors):
    return requests.get('http://httpbin.org/get', headers=data_dict.get('headers', {}), params=data_dict.get('params', {}))


@rostful_requests.with_service_schemas(HttpbinPostJson)
def httpbin_postjson_callback(data, data_dict, errors):
    print (" => {0}".format(data_dict))  # to help with debugging
    response = requests.post('http://httpbin.org/post', headers=data_dict.get('headers', {}), params=data_dict.get('params'), json=data_dict.get('json'))
    print (" <= {0}".format(response.json()))
    return response



##########
# Node
##########

class HttpbinNode(object):
    def __init__(self):
        rospy.loginfo('Httpbin node started. [' + rospy.get_name() + ']')

        rospy.Service('~ip_service', HttpbinIp, httpbin_ip_callback)
        rospy.Service('~useragent_service', HttpbinUserAgent, httpbin_useragent_callback)
        rospy.Service('~headers_service', HttpbinHeaders, httpbin_headers_callback)
        rospy.Service('~get_service', HttpbinGet, httpbin_get_callback)
        rospy.Service('~postjson_service', HttpbinPostJson, httpbin_postjson_callback)
        # TODO
        #rospy.Service('~postform_service', HttpbinPostForm, httpbin_postform_callback)
        #rospy.Service('~postfiles_service', HttpbinPostFiles, httpbin_postfiles_callback)

    def spin(self):
        rospy.spin()


if __name__ == '__main__':
    rospy.init_node('pyros_rosclient_httpbin')
    node = HttpbinNode()
    node.spin()
