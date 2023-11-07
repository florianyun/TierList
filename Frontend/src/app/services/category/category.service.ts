import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Category } from 'src/app/models/category.model';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private CategoryUrl = 'http://localhost:8000/categories'; 
  constructor(private http: HttpClient) {}
  
  public getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.CategoryUrl + '/');
  }

  public addCategory(category: Category) {
    return this.http.post(this.CategoryUrl, category);
  }

}