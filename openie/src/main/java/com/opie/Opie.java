package com.opie;

import java.util.List;

import edu.stanford.nlp.ie.util.RelationTriple;
import edu.stanford.nlp.simple.Document;
import edu.stanford.nlp.simple.Sentence;

public class Opie {
	
	

	public SubjectVerbObject getTriplesfromText(String text){
		
		SubjectVerbObject svo =  new SubjectVerbObject();
		List<Triples> svoList = svo.getSpoList();	
		
		//Document doc = new Document("V1 was northbound on a five lane, not physically divided, dry roadway, preparing to turn left at the intersection.");
		Document doc = new Document(text);
		
	    // Iterate over the sentences in the document
	    for (Sentence sent : doc.sentences()) {
	      // Iterate over the triples in the sentence
	      for (RelationTriple triple : sent.openieTriples()) {
	    	  
	    	 //System.out.println(triple.toString());
	    	 String[] split = triple.toString().split("\t");
	    	 Triples triplet = new Triples();
	    	 triplet.setSubject(split[1]);
	    	 triplet.setPredicate(split[2]);
	    	 triplet.setObject(split[3]);
	    	 
	    	 svoList.add(triplet);
	      }
	    }
		
	    svo.setLength(svoList.size());
		
		return svo;
	}
}