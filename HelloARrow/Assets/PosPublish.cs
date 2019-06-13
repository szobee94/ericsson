using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using uPLibrary.Networking.M2Mqtt;
using System;
using System.Text;
using System.Globalization;
using UnityEngine.XR.ARFoundation;
using uPLibrary.Networking.M2Mqtt.Messages;

public class PosPublish : MonoBehaviour
{

    //add PointCloud
    private float nextActionTime = 0.0f;
    public string brokerHostname = "valami";
    public int brokerPort = 1883;
    public string username = null;
    public string password = null;
    public MqttClient client;

    //message topic
    public string topic = "position";
    //message data
    //message ID
    ushort messageId;
    //Constructors, certificate

    private float period = 0.05f;
    //Ray ray;

    public void Publish(string _topic, string msg)
    {
        client.Publish(
            _topic, Encoding.UTF8.GetBytes(msg),
            MqttMsgBase.QOS_LEVEL_AT_MOST_ONCE, false);
    }

    void Connect()
    {
        client = new MqttClient(brokerHostname);
        string clientId = "UnityClient_pc" + UnityEngine.Random.Range(1, 10000);
        client.Connect(clientId, username, password);
        byte[] qosLevels = { MqttMsgBase.QOS_LEVEL_AT_LEAST_ONCE };
        client.Subscribe(new string[] { topic }, qosLevels);
    }

    // Start is called before the first frame update
    void Start()
    {
        //initPos ();
        Publish("position", "app started");

    }

    // Update is called once per frame
    void Update()
    {
        var cameraForward = Camera.current.transform.forward;
        var cameraPosition = Camera.current.transform.position;
        long timeStamp = DateTime.Now.Ticks;


        if (Time.time > nextActionTime)
        {
            nextActionTime += period;
            String xyz = timeStamp.ToString() + ',' + cameraForward.x.ToString() + ',' + cameraForward.y.ToString() + ',' + cameraForward.z.ToString() + ',' + cameraPosition.x.ToString() + ',' + cameraPosition.y.ToString() + ',' + cameraPosition.z.ToString() + ",0"; // + ',' + polarPhi.ToString();
            Publish("position/uplink", xyz);
        }

        if (client == null)
        {
            Debug.Log("No MQTT client");
            return;

        }
    }
}