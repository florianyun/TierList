import { Component, OnInit } from '@angular/core';
import { Element } from 'src/app/models/element.model';
import { ElementService } from 'src/app/services/element/element.service';
import {CdkDragDrop, moveItemInArray} from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-element-list',
  templateUrl: './element-list.component.html',
  styleUrls: ['./element-list.component.scss']
})
export class ElementListComponent implements OnInit {
  elements: Element[] = [];
  newElement: Element = { id:undefined, titre:'', groupe:'', source:''};

  constructor( private elementService: ElementService){}

  public ngOnInit() {
    this.elementService.getElements().subscribe(
      (elements)=>{this.elements=elements;}
    )
  }

  addElement(){
    this.elementService.addElement(this.newElement).subscribe(()=>{
      this.elements.push(this.newElement)
    })
  }

  deleteElement(id: number){
    this.elementService.deleteElement(id).subscribe(()=>{
      this.elements.splice(this.elements.findIndex((element)=>element.id==id),1);
    })
  }

  saveElements() {
    const updatedElements = this.elements.map((element, index) => ({ ...element, ordre: index }));
    this.elementService.updateElementList(updatedElements).subscribe();
  }  

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.elements, event.previousIndex, event.currentIndex);
  }
}
