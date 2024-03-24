import { Component, Output, EventEmitter, OnInit  } from '@angular/core';
import axios from 'axios';

@Component({
  selector: 'app-battle',
  standalone: true,
  imports: [],
  templateUrl: './battle.component.html',
  styleUrl: './battle.component.css'
})
export class BattleComponent {
  @Output() setView = new EventEmitter<boolean>();
  leftID!: string;
  rightID!: string;
  leftURL!: string;
  rightURL!: string;

  leftVotes!: string | number;
  rightVotes!: string | number;

  hasVoted: boolean = false;

  changeView(isHome: boolean) {
    this.setView.emit(isHome);
  }

  ngOnInit() {
    this.getImages();
  }

  getImages() {
    axios.get('http://127.0.0.1:5000/')
    .then((res) => {
      this.leftURL = res.data.char1_url[0]
      this.leftID = res.data.char1.id
      this.rightURL = res.data.char2_url[0]
      this.rightID = res.data.char2.id
      console.log(res.data)

      this.hasVoted = false;
    })
    .catch((err) => console.log(err));

  }


  postVotes(id: string | number) {
    this.hasVoted = true;
    axios.post('http://127.0.0.1:5000/', {
      "char1_id": this.leftID,
      "char2_id": this.rightID,
      "winner": id
    })
    .then((res) => {
      if (res.data.switch) {
        this.leftVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
      } else {
        this.leftVotes = (res.data.votes1 * 100) / (res.data.votes1 + res.data.votes2);
        this.rightVotes = (res.data.votes2 * 100) / (res.data.votes1 + res.data.votes2);
      }

      this.leftVotes = this.leftVotes + '%'
      this.rightVotes = this.rightVotes + '%'
      console.log(res.data)
    })
    .catch((err) => console.log(err));

    setTimeout(() => {
      this.getImages()
    }, 3000);
  }
}
