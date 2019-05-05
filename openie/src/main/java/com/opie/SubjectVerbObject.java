package com.opie;

import java.util.ArrayList;
import java.util.List;

public class SubjectVerbObject {

	List<Triples> spoList = new ArrayList<Triples>();;
	int length = 0;

	public int getLength() {
		return length;
	}

	public void setLength(int length) {
		this.length = length;
	}

	public List<Triples> getSpoList() {
		return spoList;
	}

	public void setSpoList(List<Triples> spoList) {
		this.spoList = spoList;
	}

}
