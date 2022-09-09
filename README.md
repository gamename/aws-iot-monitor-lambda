# aws-iot-monitor-lambda
A lambda function to monitor IoT activities and notify me via SMS if endpoints stop reporting

As of this writing, there is no good way to tell if an IoT device stops sending periodic notifications to AWS. There 
are ways to tell if an IoT device is broken, but there is not a way to detect that the device hasn't been heard from
in X number of hours.  

This lambda function is meant to fill that need.  It will scan the IoT logs for certain message strings.  If log entries 
with those strings have not been seen in 12 hours, then the function will alert me via a text message. The function 
itself will run once daily.