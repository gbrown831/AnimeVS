import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  @Output() setView = new EventEmitter<boolean>();

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

}
