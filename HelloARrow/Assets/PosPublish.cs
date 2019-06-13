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

        //private float period = 0.05f;
        //Ray ray;



    void Connect()
    {
        client = new MqttClient (brokerHostname, brokerPort, false, null);
        string clientId= "UnityClient_pc" + UnityEngine.Random.Range(1, 10000);
        client.Connect(clientId, username, password);
        client.Subscribe (topic);
    }

        // Start is called before the first frame update
    void Start()
        {
            if (brokerHostname != "none")
            {
                Debug.Log("Try to connect to " + brokerHostname + ":" + brokerPort);
                client = new MqttClient(brokerHostname, brokerPort, false, null);
                string clientId = "UnityClient_pc" + UnityEngine.Random.Range(1, 10000);
                client.Connect(clientId, username, password);
                client.Subscribe(topic);
                Debug.Log("Connected to MQTT");
            }
        //ResetMotionTracking


        }

        // Update is called once per frame
        void Update()
        {
             var cameraForward = Camera.current.transform.forward;
             var cameraPosition = Camera.current.transform.position;
             long timeStamp = DateTime.Now.Ticks; 


        }
    }