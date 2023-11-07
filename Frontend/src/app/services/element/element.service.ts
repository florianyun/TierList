import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Element } from 'src/app/models/element.model';
import { forkJoin } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ElementService {
  private ElementsUrl = 'http://localhost:8000/elements'; 
  constructor(private http: HttpClient) {}
  
  public deleteElement(id: number) {
    return this.http.delete(this.ElementsUrl + '/'+id);
  }

  public getElements(): Observable<Element[]> {
    return this.http.get<Element[]>(this.ElementsUrl + '/');
  }

  public addElement(element: Element) {
    return this.http.post(this.ElementsUrl, element);
  }

  public updateElement(element: Element): Observable<Element>{
    return this.http.put<Element>(`${this.ElementsUrl}/${element.id}`, element);
  }

  public updateElementList(elements: Element[]){
    return forkJoin(elements.map((element)=>this.updateElement(element)));
  }
}
