package org.mats990.wireless;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.UnknownHostException;


@Component
@Slf4j
public class DeviceStatusService {

    private static final String DEVICE_NAME = "OnePlus_5";

    public boolean isConnected() {
        try {
            InetAddress address = Inet4Address.getByName(DEVICE_NAME);
            boolean reachable = address.isReachable(2_000);
            return reachable;
        } catch (UnknownHostException uhe){
            return false;
        } catch (Exception e){
            log.error(e.getMessage(), e);
            return false;
        }
    }

}
