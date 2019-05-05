package com.opie;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class OpenieController {

	  @RequestMapping(method = RequestMethod.GET, value="/opie")
	  @ResponseBody
	  public SubjectVerbObject registerStudent(@RequestParam String text) {
	  
		  System.out.println("Openie Controller");
		  Opie opie = new Opie();
		  SubjectVerbObject svo = opie.getTriplesfromText(text);
		  return svo;
	  }
	
}
