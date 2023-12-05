package com.yukiiiii.knowledge;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
class FirstController {

    @RequestMapping("/test")
    public String test(){
        System.out.println("test");
        return "test";
    }
}