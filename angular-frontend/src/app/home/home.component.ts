import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  @Output() setView = new EventEmitter<boolean>();
  background!: string;

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }
 
  // ngOnInit() {
  //   this.background = `../src/assets/background_${Math.floor(Math.random() * 4)}.jpg`;
  // }

  // getBackground() {
  //   return `url(${this.background})`;
  // }

}
